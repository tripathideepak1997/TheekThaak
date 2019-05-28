from django.urls import path
from . import views

app_name = 'operations'

urlpatterns = [
    path('wishlist/add/<int:pk>/', views.add_wishlist_item, name='add_wishlist_items'),
    path('wishlist/', views.list_wishlist_items, name='wishlist'),
    path('delete-item/<int:pk>/', views.delete_wishlist_items, name='delete_wishlist_items'),
    path('orders/', views.show_orders, name='orders'),
    path('cart/', views.show_cart, name='cart'),
    path('address/', views.show_address, name='address'),
    path('track/', views.track_order, name='track'),
]