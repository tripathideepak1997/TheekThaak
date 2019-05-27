from django.urls import path
from .views import show_ordered_items,apply_coupon
app_name='orders'
urlpatterns = [
    path('', show_ordered_items, name='checkout'),
    path('apply/', apply_coupon, name='apply_name'),
]
