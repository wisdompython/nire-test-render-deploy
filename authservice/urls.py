from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import *


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/',UserRegisterAPIView.as_view(), name='login'),
    path("resend_otp/", resend_otp_token, name='resend_otp'),
    path("confirm_otp/", confirm_otp, name='confirm_otp'),
    path("user_profile/", UserProfileAPIView.as_view(), name='user_profile')
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done')
]