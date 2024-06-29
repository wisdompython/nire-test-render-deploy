from django.urls import path, include
from .views import *

urlpatterns = [
    path('dashboard/', DashBoardView.as_view()),
    path('request_pickup/', WasteBinPickupView.as_view())
]