from django.http import HttpResponse
from django.shortcuts import render
from core.models import OrderedItems, DeliveryAddresses, Customer, Wishlist


# Create your views here.


def show_ordered_items(request):
    orders = Wishlist.objects.filter(customer=request.user)
    delivery_addresses = DeliveryAddresses.objects.filter(customer=request.user)

    context = {
        'orders':orders,
        'addresses': delivery_addresses
    }
    return render(request, 'orders/checkout.html', context)

def apply_coupon(request):
    dicts = []
    coupon = request.GET['coupon']
    total = int(request.GET['total'])
    if coupon == 'FIRST':
        discount = 0.10 * total
    else:
        discount  = 0
    total = total-discount
    return HttpResponse(total)

def confirm_order(request):
    return HttpResponse('Payment now will start')



