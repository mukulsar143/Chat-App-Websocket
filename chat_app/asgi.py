import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from chats.consumers import TicketChatConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat_app.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/ticket_chat/<int:ticket_id>/", TicketChatConsumer.as_asgi()),
        ])
    ),
})
