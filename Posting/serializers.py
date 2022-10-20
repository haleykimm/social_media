from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return obj.author.username

    like = serializers.SerializerMethodField()

    def get_like(self, obj):
        return obj.like.values('username')

    def create(self, validated_data):
        user = self.context.get("request").user
        post = Post(**validated_data)
        post.author = user
        post.save()
        return post

    class Meta:
        model = Post
        fields = ["id", "author", "title", "content", "like", "post_comments"]
        extra_kwargs = {'like' :{"required": False, "allow_null": True}, "post_comments": {"required":False, "allow_null":True}}