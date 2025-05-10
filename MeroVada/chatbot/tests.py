from django.test import TestCase, Client
from django.urls import reverse
import json

class ChatbotViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.chatbot_url = reverse('chatbot_response')  
    def test_chatbot_valid_post_request(self):
        data = {"message": "Hello, what is MeroVada about?"}
        response = self.client.post(
            self.chatbot_url,
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("reply", response.json())

    def test_chatbot_invalid_get_request(self):
        response = self.client.get(self.chatbot_url)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
