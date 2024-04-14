from django.urls import path
from home.consumers import *


websocket_patterns = [
 path('ws/chat/<int:id>/', ChatConsumer.as_asgi())       
]
