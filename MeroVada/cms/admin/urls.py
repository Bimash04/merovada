# cms/admin/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # Items
    path('items/', views.manage_items, name='manage_items'),
    path('item/create/', views.create_item, name='create_item'),
    path('item/update/<int:item_id>/', views.update_item, name='update_item'),
    path('item/delete/<int:item_id>/', views.delete_item, name='delete_item'),
  
    # Users
    path('users/', views.manage_users, name='manage_users'),
    path('user/create/', views.create_user, name='create_user'),
    path('user/update/<int:user_id>/', views.update_user, name='update_user'),
    path('user/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    # Profiles
 
    # Reviews
    path('reviews/', views.manage_reviews, name='manage_reviews'),
    # path('review/create/', views.create_review, name='create_review'),
    path('review/update/<int:review_id>/', views.update_review, name='update_review'),
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),
    # Notifications
    path('notifications/', views.manage_notifications, name='manage_notifications'),
    path('careers/add-culture/', views.add_culture, name='add_culture'),
    path('careers/add-benefit/', views.add_benefit, name='add_benefit'),
    path('rental-plans/', views.manage_rental_plans, name='manage_rental_plans'),
    path('careers/post-job/', views.post_job, name='post_job'),
    
    path('about-us/add/', views.add_about_us, name='add_about_us'),
    path('about-us/edit/', views.edit_about_us, name='edit_about_us'),
    # # Orders
    path('orders/', views.manage_orders, name='manage_orders'),
]
    