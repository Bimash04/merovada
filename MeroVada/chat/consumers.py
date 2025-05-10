import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from Register.models import CustomUser
from .models import ChatMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.close()
            return

       
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]

        # Check if the room_id is valid (i.e., it contains two user IDs).
        user_ids = self.room_id.split('_')
        if str(self.user.id) == user_ids[0]:
            partner_id = user_ids[1]
        else:
            partner_id = user_ids[0]
        self.partner = await self.get_user(partner_id)

        self.room_group_name = f"chat_{self.room_id}"

        # Join the Channels group.
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group.
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]

        # Save the message.
        await self.save_message(message)

        # Broadcast the message to the group.
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender_id": self.user.id,
                "username": self.user.username,
            }
        )

    async def chat_message(self, event):
        # Send the message to the WebSocket.
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender_id": event["sender_id"],
            "username": event["username"],
        }))

    @database_sync_to_async
    def get_user(self, user_id):
        return CustomUser.objects.get(id=user_id)

    @database_sync_to_async
    def save_message(self, message):
        ChatMessage.objects.create(
            sender=self.user,
            receiver=self.partner,
            message=message
        )
