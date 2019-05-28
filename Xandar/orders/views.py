from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from core.models import OrderedItems, DeliveryAddresses, Customer, Wishlist


# Create your views here.


def show_ordered_items(request):

    if request.method == 'POST':
        pass
    else:
        #CHANGE
        orders = Wishlist.objects.filter(customer=request.user)
        delivery_addresses = DeliveryAddresses.objects.filter(customer=request.user)

        context = {
            'orders':orders,
            'addresses': delivery_addresses
        }
        return render(request, 'orders/checkout.html', context)


def apply_coupon(request):
    coupon = request.GET['coupon']
    total = int(request.GET['total'])
    if coupon == 'FIRST':
        discount = 0.10 * total
    else:
        discount  = 0
    total = total-discount
    return HttpResponse(total)


def place_order(request):
    UserAddress = DeliveryAddresses()
    context={}
    for key, values in request.GET.items():
            setattr(UserAddress, key, request.GET[key])
            context[key]=values
    UserAddress.customer = request.user
    UserAddress.save()
    #UPDATE MAKE CART
    orders = Wishlist.objects.filter(customer=request.user)
    context['orders']=orders
    return render(request, 'orders/order_confirmed.html', context)
