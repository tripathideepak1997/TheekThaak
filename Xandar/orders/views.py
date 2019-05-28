from django.http import HttpResponse
from django.shortcuts import render, redirect
from core.models import OrderedItems, DeliveryAddresses, Customer, Wishlist


# Create your views here.


def show_ordered_items(request):

    if request.method == 'POST':
        pass
    else:
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

def place_order(request):
    UserAddress = DeliveryAddresses()
    for key, values in request.GET.items():
            setattr(UserAddress, key, request.GET[key])
    UserAddress.customer = request.user
    UserAddress.save()
    #return redirect('index')
    return HttpResponse('success')

    # receiver_name = models.CharField(max_length=50, blank=False)
    # street_address = models.CharField(max_length=50, blank=False)
    # city = models.CharField(max_length=50, blank=False)
    # pincode = models.IntegerField(blank=False)
    # state = models.CharField(max_length=50, blank=False)
    # phone_number = models.IntegerField(blank=False)
    #for fields in request.GET
    # for key, items in request.GET.iteritems():
    #     print(key)
    #     print(items)

def order_success(request):
    return render(request,'orders/order_confirmed.html')