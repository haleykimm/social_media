from django.shortcuts import render, get_object_or_404
from Posting.permissions import CustomReadOnly
from .models import Post
from Comments.models import Comment
from Comments.serializers import CommentSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class CommentList(APIView):
    permission_classes = [CustomReadOnly]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        postId = request.GET.get('postId')
        post = get_object_or_404(Post, pk=postId) # 없는 포스트에 대해서는 응답하지 않음
        comment = Comment.objects.filter(post=post)
        serialized_comment_data = self.serializer_class(comment, many=True).data
        return Response(serialized_comment_data, status=status.HTTP_200_OK)

    def post(self, request):
        deserialized_comment_data = CommentSerializer(data=request.data, context={'context': request})
        if deserialized_comment_data.is_valid():
            deserialized_comment_data.save()
            return Response({"Message":"Comment posted."}, status=status.HTTP_200_OK)
        return Response({"Message":"Posting failed."}, status=status.HTTP_400_BAD_REQUEST) #serialized_post_data.errors 

class CommentDetail(APIView):
    permission_classes = [CustomReadOnly]
    authentication_classes = [JWTAuthentication]

    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        serialized_comment_data = self.CommentSerializer(comment).data
        return Response(serialized_comment_data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(request, comment) #self.request
        deserialized_comment_data = CommentSerializer(data=request.data)
        if deserialized_comment_data.is_valid():
            deserialized_comment_data.save()
            return Response({"Message":"Comment revised."}, status=status.HTTP_200_OK)
        return Response({"Message":"Revision failed."}, status=status.HTTP_400_BAD_REQUEST) # deserialized_comment_data.errors

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(request, comment) #self.request
        comment.delete()
        return Response({"Message":"Comment deleted."}, status=status.HTTP_200_OK)