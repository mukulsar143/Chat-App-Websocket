from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Message
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        if not self.scope["user"].is_authenticated:
            await self.close()
            return
        
        request_user = self.scope["user"]
        chat_with_user_id = self.scope['url_route'].get('kwargs', {}).get('id')
        
        if chat_with_user_id is None:
            await self.close()
            return
        
        try:
            chat_with_user_id = int(chat_with_user_id)
        except ValueError:
            await self.close()
            return
        
        user_ids = [request_user.id, chat_with_user_id]
        user_ids.sort()
        self.room_group_name = f'chat_{user_ids[0]}_{user_ids[1]}' 
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        if text_data is None:
            return

        try:
            data = json.loads(text_data)
            message = data.get('message')
        except json.JSONDecodeError:
            return

        if message:
            await self.save_message(message)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat.message',
                    'message': message
                }
            )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
        
    @database_sync_to_async
    def save_message(self, message):
        # Save message to database
        Message.objects.create(
            user=self.scope["user"],
            content=message
        )
