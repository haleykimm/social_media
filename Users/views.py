from os import access
from django.contrib.auth import authenticate
from django.shortcuts import get_list_or_404, render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from Users.models import User
from Users.serializers import UserSignUpSerializer, UserSearchSerializer, MyPostSerializer, MyLikeSerializer, MyCommentSerializer
from Posting.permissions import CustomReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from Posting.models import Post
from Likes.models import Like
from Comments.models import Comment

# Create your views here.
class UserSignUpView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serialized_user_data = UserSignUpSerializer(data=request.data)
        if serialized_user_data.is_valid():
            user = serialized_user_data.save()
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            return Response({
                "message": "Registered successfully.",
                "token": {"access": access_token}}, 
                status=status.HTTP_200_OK)
        return Response({"error":"실패"}, status=status.HTTP_400_BAD_REQUEST)

class UserSignInView(APIView):
    def post(self, request):
        user = authenticate(username=request.data.get("username"), password=request.data.get("password"))
        if user is not None:
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            return Response({
                "message": "Logged in.",
                "token": {"access": access_token}},
                status=status.HTTP_200_OK)
            return Response({"error": "실패"}, status=status.HTTP_400_BAD_REQUEST)

#search/user?username=username
class UserSearchList(APIView):
    def get(self, request, query):
        user_list = get_list_or_404(User, query=query)
        serialized_user_list_data = UserSearchSerializer(user_list, many=True).data
        return Response(serialized_user_list_data, status=status.HTTP_200_OK)

class UserSearchList2(APIView):
    def get(self, request):
        username = request.GET.get['username']
        queried_user_list = User.objects.filter(username__icontains=username)
        serialized_queried_user_list = UserSearchSerializer(queried_user_list, many=True).data
        return Response(serialized_queried_user_list, status=status.HTTP_200_OK)


#my/
class MyPage(APIView):
    permission_classes = [CustomReadOnly]
    authentication_classes = [JWTAuthentication]

#my/my_info
class MyInfo(APIView):
    def get(self, request):
        username = request.user
        my_info = User.objects.get(username__exact=username)
        serialized_my_info = UserSearchSerializer(my_info, many=True).data
        return Response(serialized_my_info, status=status.HTTP_200_OK)

#my/my_posts
class MyPostList(APIView):
    def get(self, request):
        username = request.user #str
        user_id = User.objects.values(username__exact=username)['id']
        my_posts = Post.objects.filter(author__exact=user_id)
        serialized_my_likes = MyPostSerializer(my_posts, many=True).data
        return Response(serialized_my_likes, status=status.HTTP_200_OK)

#my/my_likes
class MyLikeList(APIView):
    def get(self, request):
        username = request.user #str
        #user에서 username의 id를 찾는 과정 필요
        user_id = User.objects.values(username__exact=username)['id']
        my_likes = Like.objects.filter(username__exact=user_id) #Like 모델의 username 필드는 user 테이블의 pk, 즉 숫자(id)로 되어 있음
        serialized_my_likes = MyLikeSerializer(my_likes, many=True).data
        return Response(serialized_my_likes, status=status.HTTP_200_OK)

#my/my_comments
class MyCommentList(APIView):
    def get(self, request):
        username = request.user
        user_id = User.objects.filter(username__exact=username)['id']
        my_comments = Comment.objects.filter(author__exact=user_id)
        serialized_my_comments = MyCommentSerializer(my_comments, many=True).data
        return Response(serialized_my_comments, status=status.HTTP_200_OK)