from django.urls import path
from .views import *
urlpatterns = [
    path('register/', userregister, name='register'),
    path('login/', userlogin, name='login'),
]
