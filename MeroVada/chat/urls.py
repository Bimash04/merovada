
from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chat_list, name='chat_list'),
    path('chat/<int:other_user_id>/', views.chat_list, name='chat_room'),
]