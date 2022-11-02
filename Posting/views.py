from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from Posting.permissions import CustomReadOnly
from Posting.serializers import PostSerializer
from .models import Post
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.
class PostList(APIView):
    permission_classes = [CustomReadOnly]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        if not request.GET.keys():
            all_posts = Post.objects.all()
            serialized_all_posts = PostSerializer(all_posts, many=True).data
            return Response(serialized_all_posts, status=status.HTTP_200_OK)
        else:
            for query in request.GET.keys():
                query_results = Post.objects.filter(title__icontains=request.GET.get('title',''),
                                                    content__icontains=request.GET.get('content',''),
                                                    author__username__icontains=request.GET.get('author',''))
                if query_results:
                    serialized_query_results = PostSerializer(query_results, many=True).data
                    return Response(serialized_query_results, status=status.HTTP_200_OK)
                else: 
                    return Response({"message":"No post matching the query."}, status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        deserialized_post_data = PostSerializer(data=request.data, context={'request': request})
        if deserialized_post_data.is_valid():
            deserialized_post_data.save()
            return Response({"message":"Posted."}, status=status.HTTP_200_OK)
        return Response(deserialized_post_data.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetail(APIView):
    permission_classes = [CustomReadOnly]
    authentication_classes = [JWTAuthentication]

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serialized_post_data = PostSerializer(post).data
        return Response(serialized_post_data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, post)
        serialized_post_data = PostSerializer(post, data=request.data)
        if serialized_post_data.is_valid():
            serialized_post_data.save()
            return Response(serialized_post_data.data)
        return Response(serialized_post_data.errors, status=status.HTTP_400_BAD_REQUEST)
       
    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, post)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LikeDetail(APIView):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if request.user in post.like.all():
            post.like.remove(request.user)
            return Response({'message':'Like cancelled.'}, status=status.HTTP_200_OK)
        else: 
            post.like.add(request.user)
            return Response({'message': 'Post liked.'}, status=status.HTTP_200_OK)