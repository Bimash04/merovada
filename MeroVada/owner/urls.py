from django.urls import path
from . import views

urlpatterns = [
   
    path('pending-items/', views.pending_items, name='pending_items'),
    path('approve-item/<int:item_id>/', views.approve_item, name='approve_item'),
    path('reject-item/<int:item_id>/', views.reject_item, name='reject_item'),
    path('owner-dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('update-status/<int:item_id>/<str:status>/', views.update_status, name='update_status'),
    path('edit-item/<int:item_id>/', views.edit_item, name='edit_item'),
    path('delete-item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('add/', views.add_item, name='add_item'),
    path('list/', views.list_items, name='list_items'),
    path('edit/<int:item_id>/', views.edit_item, name='edit_item'),
    path('delete/<int:item_id>/', views.delete_item, name='delete_item'),
]