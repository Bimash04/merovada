from django.urls import path
from . import views

urlpatterns = [
    path('blog', views.blog_list, name='blog_list'),
    path('post/<int:post_id>/', views.blog_detail, name='blog_detail'),
    path('submit/', views.submit_blog, name='submit_blog'),
]