from rest_framework.permissions import BasePermission
from rest_framework.exceptions import APIException
from rest_framework import status

class GenericAPIException(APIException):
    def __init__(self, status_code, detail=None, code=None):
        self.status_code=status_code
        super().__init__(detail=detail, code=code)

class CustomReadOnly(BasePermission):
    SAFE_METHODS = ('GET',)
    message = 'Authorization required.'

    def has_permission(self, request, view):
        user = request.user
        if request.method in self.SAFE_METHODS:
            return True
        elif user.is_authenticated:
            return True
        elif not user.is_authenticated:
            response = {
                "detail": "Please sign in.",
            }
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)
        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method in self.SAFE_METHODS:
            return True
        elif hasattr(obj, 'author'):
            return obj.author == user
        return False    
