from django.urls import path
from .views import show_ordered_items,apply_coupon, place_order, order_success
app_name='orders'
urlpatterns = [
    path('', show_ordered_items, name='checkout'),
    path('apply/', apply_coupon, name='apply_name'),
    path('place_order/',place_order, name='place_order'),
    path('order-confirmed/', order_success, name='order_success')
]
