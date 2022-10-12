from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from Likes.serializers import LikeSerializer
from Posting.permissions import CustomReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from Posting.models import Post
from Likes.models import Like

# Create your views here.
class LikeView(APIView):
    permission_classes = [CustomReadOnly]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        deserialized_like_data = LikeSerializer(data=request.data, context={'request': request})
        if deserialized_like_data.is_valid():
            deserialized_like_data.save()
            return Response(status=status.HTTP_200_OK)
        return Response(deserialized_like_data.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete 요청(포스트, 토큰) -> 라이크 한 사람 확인 - > like한 유저 중 있는지 확인 -> 있을 경우 해당 like DB에서 삭제 
    def delete(self, request, pk):
        like = get_object_or_404(Like, pk=pk)
        self.check_object_permissions(like, request)
        like.delete()
        return Response(status=status.HTTP_200_OK)
