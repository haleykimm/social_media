from .models import Comment
from rest_framework import serializers

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    
    def get_author(self, obj):
        return obj.author.username

    def create(self, validated_data): #comment 객체 생성
        user = self.context.get('request').user
        comment = Comment(**validated_data)
        comment.author = user
        comment.save()
        return comment

    class Meta:
        model = Comment
        field = ['post_id', 'id', 'author', 'content']
        extra_kwargs = {'post': {'write_only': True}}