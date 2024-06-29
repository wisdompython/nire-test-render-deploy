from rest_framework import serializers
from .models import *
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenObtainPairSerializer
import secrets

import time
import random

class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser  
        fields=("email", "password", "confirm_password")
        extra_kwargs = {'password': {'write_only': True}, # key word argument
                        "confirm_password":{'write_only':True}}
        
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
            {"password": "Password fields didn't match."})
       
        try:
            validate_password(attrs['password'])
        except ValidationError as err:
            raise serializers.ValidationError(
            {"password": err.messages})
        return attrs
    def create(self, validated_data):
        
        new_user = CustomUser.objects.create(
            email = validated_data['email'],
        )
        new_profile = UserProfile.objects.create(user=new_user)
        new_user.set_password(validated_data['password'])
        new_user.save()
        return new_user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        label='username or password'
    )
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs['username']
        password = attrs['password']


        if username and password:
            user = authenticate(
                username=username, password=password,request=self.context.get('request')
            )

            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs



class ConfirmOTPSerializer(serializers.Serializer):
    otp = serializers.CharField()
    email = serializers.EmailField()


class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()


class UpdateUserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = "__all__"

    def validate(self, attrs):
        if 'phone_number' in attrs.keys() or 'email' in attrs.keys():
            raise serializers.ValidationError(
            {"error": "You cannot update your phone number or email address "})
        return attrs 
    
class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        fields = ['password', 'confirm_password']

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        user = self.context.get('user')
        if password != confirm_password:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        user.set_password(password)
        user.save()
        return attrs
    

# class SendPasswordResetEmailSerializer(serializers.Serializer):
#   email = serializers.EmailField(max_length=255)
#   class Meta:
#     fields = ['email']

#   def validate(self, attrs):
#     email = attrs.get('email')
#     if User.objects.filter(email=email).exists():
#       user = User.objects.get(email = email)
#       uid = urlsafe_base64_encode(force_bytes(user.id))
#       print('Encoded UID', uid)
#       token = PasswordResetTokenGenerator().make_token(user)
#       print('Password Reset Token', token)
#       link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
#       print('Password Reset Link', link)
#       # Send EMail
#       body = 'Click Following Link to Reset Your Password '+link
#       data = {
#         'subject':'Reset Your Password',
#         'body':body,
#         'to_email':user.email
#       }
      
#       return attrs
#     else:
#       raise serializers.ValidationError('You are not a Registered User')

class UserPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

     