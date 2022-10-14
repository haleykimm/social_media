from os import access
from django.contrib.auth import authenticate
from django.shortcuts import get_list_or_404, render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from Users.models import User
from Users.serializers import UserSignUpSerializer, UserSerializer
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


'''
class UserSearchList2(APIView):
    def get(self, request, query):
        username = request.GET.get['username']
        user_list = get_list_or_404(User, query=username)
        serialized_user_list_data = UserSearchSerializer(user_list, many=True).data
        return Response(serialized_user_list_data, status=status.HTTP_200_OK)
'''
class UserSearchList(APIView):
    def get(self, request):
        username = request.GET.get('username')
        if not username == None:
            query_result = User.objects.filter(username__icontains=username)
            serialized_query_result = UserSerializer(query_result, many=True).data
            return Response(serialized_query_result, status=status.HTTP_200_OK)
        else:
            return Response({"message":"No user matching the query."}, status=status.HTTP_204_NO_CONTENT)

class MyInfo(APIView):
    permission_classes = [CustomReadOnly]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        username = request.user.username
        my_info = User.objects.filter(username__exact=username)
        serialized_my_info = UserSerializer(my_info, many=True).data
        return Response(serialized_my_info, status=status.HTTP_200_OK)