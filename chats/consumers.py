from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import SupportTicket, TicketMessage
from channels.db import database_sync_to_async

class TicketChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.ticket_id = self.scope["url_route"]["kwargs"]["ticket_id"]
        self.room_group_name = f"ticket_{self.ticket_id}"

        # Ensure the user is authenticated
        user = self.scope.get("user")
        if not user or not user.is_authenticated:
            await self.close()
            return

        try:
            # Get the ticket asynchronously
            self.ticket = await self.get_ticket(self.ticket_id)
        except SupportTicket.DoesNotExist:
            await self.close()
            return

        # Use sync_to_async to get the customer and assigned agent
        customer = await self.get_customer(self.ticket)
        assigned_agent = await self.get_assigned_agent(self.ticket)

        # Role-based access check (Customer or Agent)
        if customer == user or assigned_agent == user:
            # Join the room group for both customer and assigned agent
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Parse incoming message
        data = json.loads(text_data)
        message = data.get("message")
        sender = self.scope.get("user")  # Fetch the authenticated user

        if not message or not sender:
            return

        # Save the message asynchronously
        await self.create_ticket_message(self.ticket, sender, message)

        # Send the message to the group (other users in the room)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender.username,  # Send the sender's username, or any other info needed
            }
        )

    async def chat_message(self, event):
        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],  # Use the correct sender (username)
        }))

    # Asynchronous method to fetch the ticket
    @database_sync_to_async
    def get_ticket(self, ticket_id):
        try:
            return SupportTicket.objects.get(id=ticket_id)
        except SupportTicket.DoesNotExist:
            return None

    # Asynchronous method to get the customer associated with the ticket
    @database_sync_to_async
    def get_customer(self, ticket):
        return ticket.customer

    # Asynchronous method to get the assigned agent associated with the ticket
    @database_sync_to_async
    def get_assigned_agent(self, ticket):
        return ticket.assigned_agent

    # Asynchronous method to create a ticket message
    @database_sync_to_async
    def create_ticket_message(self, ticket, sender, message):
        return TicketMessage.objects.create(
            ticket=ticket,
            sender=sender,  # Ensure sender is passed as the actual user (request.user)
            message=message
        )
