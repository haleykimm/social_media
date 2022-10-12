from rest_framework import serializers
from .models import Like
from Posting.models import Post   

class LikeSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        username = obj.username.username

    def create(self, validated_data):
        user = self.context.get('request').user
        like = Like(**validated_data)
        like.username = user
        return like

    class Meta:
        model = Like
        fields = ['post_id', 'username']