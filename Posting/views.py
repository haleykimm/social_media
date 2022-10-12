from optparse import TitledHelpFormatter
from turtle import title
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from Posting.permissions import CustomReadOnly
from Posting.serializers import PostSerializer
from .models import Post
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q

# Create your views here.
class PostList(APIView):
    permission_classes = [CustomReadOnly]
    authentication_classes = [JWTAuthentication]

    def get(self, request): 
        post = Post.objects.all()
        serialized_post_data = PostSerializer(post, many=True).data
        return Response(serialized_post_data, status=status.HTTP_200_OK)

    def post(self, request):
        deserialized_post_data = PostSerializer(data=request.data, context={'request': request})
        if deserialized_post_data.is_valid():
            deserialized_post_data.save()
            return Response({"message":"정상"}, status=status.HTTP_200_OK)
        return Response (deserialized_post_data.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetail(APIView):
    permission_classes = [CustomReadOnly]
    authentication_classes = [JWTAuthentication]

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serialized_post_data = self.PostSerializer(post).data
        return Response(serialized_post_data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, post)
        serialized_post_data = self.PostSerializer(post, data=request.data)
        if serialized_post_data.is_valid():
            serialized_post_data.save()
            return Response(serialized_post_data.data)
        return Response(serialized_post_data.errors, status=status.HTTP_400_BAD_REQUEST)
       
    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, post)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#search/post?title=title&content=content&author=username
class PostSearchList(APIView):
    permission_classes = [CustomReadOnly]
    authentication_classes = [JWTAuthentication]

    def get(self, request, query):
        queried_list = get_list_or_404(Post, query=query)
        serialized_queried_list_data = PostSerializer(queried_list, many=True).data
        return Response(serialized_queried_list_data, status=status.HTTP_200_OK)

class PostSearchList2(APIView):
    permission_classes = [CustomReadOnly]
    authentication_classes = [JWTAuthentication]

#search/post?title=title
    def get(self, request):
        title = request.GET.get['title']
        queried_result = Post.objects.all().filter(title__icontains=title).order_by('updated_at')
        serialized_queried_result = PostSerializer(queried_result, many=True).data
        return Response(serialized_queried_result, status=status.HTTP_200_OK)

#search/post?content=content
    def get(self, request):
        content = request.GET.get['content']
        queried_result = Post.objects.all().filter(content__icontains=content).order_by('updated_at')
        serialized_queried_result = PostSerializer(queried_result, many=True).data
        return Response(serialized_queried_result, status=status.HTTP_200_OK)

#search/post?title=title&content=content
    def get(self, request):
        title = request.GET.get['title']
        content = request.GET.get['content']
        queried_result = Post.objects.all().filter(Q(title__icontains=title)|Q(content__icontains=content)).order_by('updated_at')
        serialized_queried_result = PostSerializer(queried_result, many=True).data
        return Response(serialized_queried_result, status=status.HTTP_200_OK)

#search/post?author=username
    def get(self, request):
        username = request.GET.get['author']
        queried_result = Post.objects.all().filter(author__icontains=username).order_by('updated_at')
        serialized_queried_result = PostSerializer(queried_result, many=True).data
        return Response(serialized_queried_result, status=status.HTTP_200_OK)