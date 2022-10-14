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
        fields = ['username', 'email', 'join_date', 'birthday', 'user_posts', 'user_likes', 'user_comments']