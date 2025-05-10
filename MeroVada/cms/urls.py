from django.urls import path, include
from . import views
urlpatterns = [
path('admin/', include('cms.admin.urls')),
path('secure_payment/', views.secure_payment, name='secure-payments'),
    path('quantity/', views.quantity, name='quality-control'),
    path('easy_return/', views.easy_return, name='easy-returns'),
    path('free_delivery/', views.free_delivery, name='free-delivery'),
]