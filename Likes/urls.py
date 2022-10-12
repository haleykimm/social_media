from django.urls import path
from Likes.views import LikeView

urlpatterns = [
    path('', LikeView.as_view())
]