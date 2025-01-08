from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/ticket_chat/(?P<ticket_id>\d+)/$', consumers.TicketChatConsumer.as_asgi()),
]
