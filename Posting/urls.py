from django.urls import path
from Posting.views import PostList, PostDetail, PostSearchList

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    path('search/?title=<str:title>&content=<str:content>&username=<str:username>', PostSearchList.as_view())
]