from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    )
from Comments.views import CommentList, CommentDetail

urlpatterns = [
    path("", CommentList.as_view()),
    path("<int:pk>", CommentDetail.as_view())
]
