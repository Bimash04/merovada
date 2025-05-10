from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import ChatMessage
from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async
import json
from django.contrib.auth.models import AnonymousUser
from chat.routing import websocket_urlpatterns
from chat.consumers import ChatConsumer
from MeroVada.asgi import application  

CustomUser = get_user_model()

class ChatTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = CustomUser.objects.create_user(username="user1", password="testpass123")
        self.user2 = CustomUser.objects.create_user(username="user2", password="testpass123")
        self.chat_url = reverse('chat_list')  

    def test_chat_list_view_authenticated(self):
        self.client.login(username="user1", password="testpass123")
        response = self.client.get(self.chat_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat_list.html')

    def test_chat_list_view_unauthenticated(self):
        response = self.client.get(self.chat_url)
        self.assertRedirects(response, '/login/?next=' + self.chat_url)

    def test_ajax_search_chat_partners(self):
        self.client.login(username="user1", password="testpass123")
        ChatMessage.objects.create(sender=self.user1, receiver=self.user2, message="Hello!")

        response = self.client.get(self.chat_url, {'search': 'user2'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue('partners' in data)
        self.assertEqual(len(data['partners']), 1)
        self.assertEqual(data['partners'][0]['username'], 'user2')

    async def test_send_and_receive_message(self):
        communicator = WebsocketCommunicator(application, f"/ws/chat/{self.user1.id}_{self.user2.id}/")
        # Force authenticate
        communicator.scope['user'] = self.user1

        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        await communicator.send_json_to({
            'message': 'Test message via WebSocket'
        })

        response = await communicator.receive_json_from()
        self.assertEqual(response['message'], 'Test message via WebSocket')
        self.assertEqual(response['username'], 'user1')

        # Check message saved to database
        messages = await sync_to_async(ChatMessage.objects.all)()
        self.assertEqual(await sync_to_async(messages.count)(), 1)

        await communicator.disconnect()

    async def test_invalid_user_in_websocket(self):
        communicator = WebsocketCommunicator(application, "/ws/chat/invalid_room/")
        communicator.scope['user'] = AnonymousUser()

        connected, _ = await communicator.connect()
        self.assertFalse(connected)

    async def test_message_saving_in_db(self):
        await sync_to_async(ChatMessage.objects.create)(
            sender=self.user1,
            receiver=self.user2,
            message="Database save test"
        )
        messages = await sync_to_async(ChatMessage.objects.all)()
        self.assertEqual(await sync_to_async(messages.count)(), 1)
        msg = await sync_to_async(messages.first)()
        self.assertEqual(msg.message, "Database save test")
