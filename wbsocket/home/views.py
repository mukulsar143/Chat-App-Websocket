from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics
from .models import *


# Create your views here.

User = get_user_model()


class GetUser(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user_obj = User.objects.exclude(id = request.user.id)
            serializer = ChatSerializer(user_obj, many = True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({'errors' : str(e)}, status=404)        
        


class MessageListCreateAPIView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated] 