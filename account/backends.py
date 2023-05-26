from typing import Any, Optional
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.http.request import HttpRequest
from rest_framework.authtoken.models import Token
from django.contrib.auth.backends import BaseBackend

class CaseInsensitiveModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None,**kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            case_insensitive_username_field = '{}__iexact'.format(UserModel.USERNAME_FIELD)
            user = UserModel._default_manager.get(**{case_insensitive_username_field: username})
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user



class TokenAuthenticationBackend(BaseBackend):
    def authenticate(self, request, id=None, auth_token=None):
        UserModel = get_user_model()

        try:
            # Get the user based on the provided id
            user = UserModel.objects.get(id=id)
        except UserModel.DoesNotExist:
            return None

        try:
            # Get the token associated with the user
            token = Token.objects.get(user_id=id)
        except Token.DoesNotExist:
            return None

        # Check if the provided token matches the user's token
        if auth_token == token.key:
            return user

        return None

    