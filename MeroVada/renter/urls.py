from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from cms.views import contact_support
from .views import LogoutView
urlpatterns = [
    path("", views.home, name="home"),
    path('filtered-items/', views.filtered_items, name='filtered_items'),
    path('products/<int:id>/', views.item_detail, name='product_desc'),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('update_cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    path('rental_dashboard', views.rental_dashboard, name='rental_dashboard'),
    path('careers/', views.careers, name='careers'),
    path('proceed_to_checkout/<int:item_id>/', views.proceed_to_checkout, name='proceed_to_checkout'),
    
    path('filtered-items/', views.filtered_items, name='filtered_items'),
    path('category/<str:category>/', views.category_items, name='category_items'),
    path('contact_us/', views.contact_us, name='contact_us'),
   
    path('about_us/', views.about_us, name='about_us'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('contact_support/', contact_support, name='contact_support'),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)