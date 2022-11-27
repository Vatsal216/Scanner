from .views_api import *
from django.urls import path, include
from rest_framework import routers



router = routers.DefaultRouter()


urlpatterns = [
 
    path('Lux_Bhoomi_View',Lux_Bhoomi_View),
]