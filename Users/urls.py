from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    )
from Users.views import UserSignUpView, UserSignInView, UserSearchList, MyInfo
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', UserSignUpView.as_view()), 
    path('signin/', UserSignInView.as_view()),
    path('my_info/', MyInfo.as_view()),
    path('user_search/', UserSearchList.as_view())
]