from xml.etree.ElementTree import Comment
from rest_framework import serializers
from Users.models import User
from Posting.models import Post
from Likes.models import Like


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, *args, **kwargs):
        user = super().create(*args, **kwargs)
        pw = user.password
        user.set_password(pw)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'user_posts', 'user_likes']

class MyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'user_posts', 'user_likes']

class MyPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'user_posts']

class MyLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'user_likes']

class MyCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'user_comments']