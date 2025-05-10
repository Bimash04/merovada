from django.urls import path
from . import views

urlpatterns = [
  
    path('payment-success/', views.payment_success, name='payment_success'),
    path('checkout/<int:item_id>/', views.checkout, name='checkout'),
    path('verify-khalti/<int:order_id>/', views.verify_khalti, name='verify_khalti'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('payment-failed/', views.payment_failed, name='payment_failed'),
    
    path('download-payment-confirmation/<int:order_id>/', views.download_payment_confirmation, name='download_payment_confirmation'),
]
