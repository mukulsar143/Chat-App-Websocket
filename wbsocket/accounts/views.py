from rest_framework.decorators import api_view
from .serializers import *
from rest_framework.response import Response
from .tokenauthentication import JWTAuthentication
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

@api_view(['POST'])
def userregister(request):
    serializer = UserSerialzer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message' : 'Sign In Successfullfy',
            'user' : serializer.data,
            'success' : True
        }, status=201)
    return Response(serializer.errors, status=404)

@api_view(['POST']) 
def userlogin(request):
    serializer = LoginSerializer(data = request.data)
    if serializer.is_valid():
        email = serializer.data['email']
        user = User.objects.filter(email = email).first()                
        user.save()
        token = JWTAuthentication.generate_token(payload=serializer.data)
        return Response({
            'message' : 'Login Successfullfy',
            'token' : token,
            'success' : True,
            'user' : serializer.data
        }, status=201)

    return Response(serializer.errors, status=404)    