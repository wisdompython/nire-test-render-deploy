from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from .models import *

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view

# serilaizer
from .serializers import *

from .utils import *

class UserRegisterAPIView(APIView):
    def post(self, request, *args, **kargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            send_otp = send_mail_to_user(serializer.data['email'])
            
            response = {
                'success': True,
                'user': serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        raise ValidationError(
            serializer.errors, code=status.HTTP_406_NOT_ACCEPTABLE)
    
class UserLoginAPIView(APIView):
    def post(self, request, *args, **kargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            response = {
                "username": {
                    "detail": "User Does not exist!"
                }
            }
            if CustomUser.objects.filter(username=request.data['email']).exists():
                user = CustomUser.objects.get(username=request.data['email'])
                
                response = {
                    'success': True,
                    'username': user.username,
                    'email': user.email,
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def resend_otp_token(request, *args, **kwargs):

    serializers = ResendOTPSerializer(data=request.data)

    if serializers.is_valid():
        get_user = CustomUser.objects.filter(email=serializers.data['email']).exists() # true or false

        if get_user:
            get_user = CustomUser.objects.get(email=serializers.data['email']) 
            send_email_with_otp = send_mail_to_user(get_user.email)
            return Response("OTP has been sent")
        
        return Response("wrong email")
    return Response(serializers.errors)


@api_view(["POST"])
def confirm_otp(request):

    serializer = ConfirmOTPSerializer(data = request.data)

    if serializer.is_valid():

        confirm_otp_code = totp.verify(serializer.data['otp'])

        if confirm_otp_code:
            verified_user = CustomUser.objects.get(email=serializer.data['email'])
            verified_user.verified = True
            verified_user.save()

    
            return Response("You are now verified")
        else:
            return Response(
                "Otp expired or incorrect"
            )
    return Response(serializer.errors)

class UserProfileAPIView(APIView):

    permission_classes = (IsAuthenticated,)
    queryset = CustomUser.objects.all()
    def get(self, request):
        print(request.user)
        user = CustomUser.objects.get(email=request.user.email)

        return Response(
            {
            'email':user.email,
            'full_name': user.full_name,
            'phone_number': user.phone_number
            }
        )
    
    def put(self,request):
        get_user = CustomUser.objects.get(id=request.user.id)
        serializers = UpdateUserProfileSerializer(get_user, data= request.data, partial=True)

        if serializers.is_valid():
   
            serializers.save()

            return Response(
                serializers.data
            )
        return Response(
            serializers.errors
        ) 
    

# class UserPasswordResetAPIView(APIView):
    