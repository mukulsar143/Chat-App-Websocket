from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'first_name', 'last_name']
        extra_kwargs = {'id' : {'read_only':True}}
        
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'user', 'content', 'timestamp']