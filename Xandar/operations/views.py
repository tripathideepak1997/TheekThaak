from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView
from core.models import Product, ProductImage
from core.models import Customer, Wishlist
# Create your views here.


@login_required
def list_wishlist_items(request):
    try:
        user = Customer.objects.get(email=request.user.email)
        items = Wishlist.objects.filter(customer=request.user)
        if not len(items) == 0:
            context = {'items': items}
        else:
            context = {'no_item_found': True}
    except Customer.DoesNotExist:
        return redirect('accounts:login_app')
    return render(request, 'operations/wishlist.html', context)


def add_wishlist_item(request, pk):
    if request.user.is_authenticated:
        product = Product.objects.get(id=pk)
        try:
            Wishlist.objects.get(product=product)
            return 'Item Already Exists in your Wishlist'
        except Wishlist.DoesNotExist:
            image = ProductImage.objects.filter(product=product).first()
            Wishlist.objects.create(customer=request.user, product=product, product_image=image)
            print('been here')
            return 'Item Added To Wishlist successfully'
    else:
        return 'Login To Save This to your Wishlist'





@login_required
def delete_wishlist_items(request, pk):
    try:
        user = Customer.objects.get(email=request.user.email)
        items = Wishlist.objects.filter(customer=request.user)
        context = {'items': items}
        # import pdb; pdb.set_trace()
        if not len(items) == 0:
            if request.method == 'POST':
                Wishlist.objects.filter(id=pk).delete()
                context = {'items': items}
        else:
            context = {'no_item_found': True}
        return HttpResponse(list_wishlist_items(request))
    except Customer.DoesNotExist:
        return redirect('accounts:login_app')


def show_orders(request):
    return render(request, 'operations/orders.html')


def show_cart(request):
    return render(request, 'operations/cart.html')


def show_address(request):
    return render(request, 'operations/address.html')


def track_order(request):
    return render(request, 'operations/track.html')