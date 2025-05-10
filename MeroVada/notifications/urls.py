from django.urls import path
from . import views
from .views import add_review, product_detail  

urlpatterns = [
    path('product/<int:item_id>/', product_detail, name='product_desc'), 
    path('product/<int:item_id>/add_review/', add_review, name='add_review'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/<int:notification_id>/mark_as_read/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('notifications/<int:notification_id>/delete/', views.delete_notification, name='delete_notification'),
    path('notifications/<int:notification_id>/edit/', views.edit_notification, name='edit_notification'),
    
    path ('help_centre',views.help_centre, name='help_centre'),
    
]