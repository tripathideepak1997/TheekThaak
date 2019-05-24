from django.urls import path
from . import views

app_name = 'operations'

urlpatterns = [
    path('wishlist/add/<int:pk>/', views.add_wishlist_item, name='add_wishlist_items'),
    path('wishlist/', views.list_wishlist_items, name='wishlist'),
    path('delete-item/<int:pk>/', views.delete_wishlist_items, name='delete_wishlist_items'),
    # path('wishlist/', views.ListWishlistItems.as_view(), name='list_wishlist_items'),
    # path('detail/<int:pk>/', views.DetailWishlistItems.as_view(), name='detail_wishlist_items'),
    # path('delete/<int:pk>/', views.DeleteWishlistItems.as_view(), name='delete_wishlist_items'),
]
