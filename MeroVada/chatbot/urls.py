from django.urls import path
from . import views

urlpatterns = [
    path("chatbot/", views.chatbot_response, name="chatbot_response"),
    path("", views.chat_page, name="chat_page"),
]