"""
ASGI config for wbsocket project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from django.urls import path
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from home.route import *
from channels.auth import AuthMiddlewareStack
from home.channels_middleware import JWTWebsocketMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wbsocket.settings')



application = ProtocolTypeRouter({
    'http' : get_asgi_application(),
    'websocket' : JWTWebsocketMiddleware(AuthMiddlewareStack(URLRouter(websocket_patterns)))
})