#this file contains the logic for a user to login with their email or password

from django.contrib.auth.backends import BaseBackend, ModelBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import *
from django.http import HttpRequest

UserModel = get_user_model()

class EmailPhoneNumberBackend(ModelBackend):

     def authenticate(self, request, username=None, password=None, **kwargs):

        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
            print(username)
        if username is None or password is None:
            return
        
        try:
            user = CustomUser.objects.get(
                Q(email=username) | Q(phone_number=username)
            )
        except UserModel.DoesNotExist:
            return "Invalid user credentials"

        if user.check_password(password):
            return user