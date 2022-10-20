from django.urls import path
from Posting.views import LikeDetail, PostList, PostDetail, LikeDetail

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    path('<int:pk>/like/', LikeDetail.as_view())
]