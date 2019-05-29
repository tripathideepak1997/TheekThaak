from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView

from Xandar import settings
from core.models import Product, ProductImage, Cart, Items
from core.models import Customer, Wishlist
# Create your views here.
from operations.forms import UpdateCartForm


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


def show_address(request):
    return render(request, 'operations/address.html')


def track_order(request):
    return render(request, 'operations/track.html')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def add_to_cart(request, product_id, quantity=1):
    errors = ""
    print('inside')
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, "You are trying to add product that does not exist")
        return render(
            request, 'operations/cart.html')

    product_image = product.productimage_set.all()[0]

    if request.user.is_authenticated:

        try:
            cart = Cart.objects.get(user=request.user, is_ordered=False)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user)

        try:
            obj = Items.objects.get(cart=cart, product=product)
            if obj:
                return "You are adding the item that already exist"
        except:
            if quantity <= product.quantity :
                if quantity <= 3:
                    Items.objects.create(cart=cart, product=product, product_img=product_image, quantity=quantity,
                                     unit_price=product.price)
                else:
                    return "This item cannot be added more than 3"
                # return something
            else:
                return 'This item is not available that much you want to avail Sorry !!!!'
                # return render(
                #     request, 'operations/cart.html')

    else:

        ip_address = get_client_ip(request)

        request.session[settings.CART_SESSION_ID] = request.session.get(settings.CART_SESSION_ID, {})

        product_id = str(product_id)

        if request.session[settings.CART_SESSION_ID] is None:
            request.session[settings.CART_SESSION_ID] = {}
            request.session[settings.CART_SESSION_ID][product_id] = {
                'product': {'id': product_id, 'name': product.name},
                'quantity': 0, 'unit_price': product.price,
                'product_img': {'image': {'url': product_image.image.url}}
            }

        elif product_id not in request.session[settings.CART_SESSION_ID]:
            request.session[settings.CART_SESSION_ID][product_id] = {
                'product': {'id': product_id, 'name': product.name},
                'quantity': 0, 'unit_price': product.price,
                'product_img': {'image': {'url': product_image.image.url}}
            }
        else :
            return "You are adding the item that already exist"

        if quantity <= product.quantity :

            if quantity <=3:
                request.session[settings.CART_SESSION_ID][product_id]['quantity'] = quantity
                request.session.modified = True
            else:
                return "This item cannot be added more than 3 in cart"
        else:
            return 'This item is not available that much you want to avail Sorry !!!!'
    return 'Item added to Cart Successfully'


def get_cart(request):
    errors = ""
    form = UpdateCartForm()
    if request.user.is_authenticated:

        '''Code to add the anonymous cart items to the logged in user'''
        # request.session[settings.CART_SESSION_ID] = request.session.get(settings.CART_SESSION_ID, None)
        # if request.session[settings.CART_SESSION_ID]:
        #     try:
        #         cart = Cart.objects.filter(user=request.user, is_ordered=False)[0]
        #     except Cart.DoesNotExist:
        #         cart = Cart.objects.create(user=request.user)
        #
        #     for item in request.session[settings.CART_SESSION_ID].values():
        #         product = Product.objects.get(id=int(item['product']['id']))
        #         product_image = product.productimage_set.all()[0]
        #         Items.objects.create(cart=cart, product=product,
        #                              product_img=product.productimage_set.all()[0], quantity=item['quantity'],
        #                              unit_price=product.price)
        #     request.session[settings.CART_SESSION_ID] = {}
        #     request.session.modified = True

        try:
            cart = Cart.objects.get(user=request.user, is_ordered=False)
            print('run')
        except Cart.DoesNotExist:
            messages.error(request, "You don't have anything in cart")
            return render(request, 'operations/cart.html', {'errors': errors})

        items = Items.objects.filter(cart=cart)
        if len(items) == 0:
            errors = "You don't have anything in cart"
        total_price = sum(Decimal(item.unit_price) * item.quantity for item in items)

    else:
        items = []
        request.session[settings.CART_SESSION_ID] = request.session.get(settings.CART_SESSION_ID, None)
        if not request.session[settings.CART_SESSION_ID]:
            errors = "You don't have anything in cart"
            return render(
                request, 'operations/cart.html', {'errors': errors})

        for item in request.session[settings.CART_SESSION_ID].values():
            # item['price'] = Decimal(item['price'])
            item['total_price'] = item['unit_price'] * item['quantity']
            items.append(item)

        total_price = sum(Decimal(item['unit_price']) * item['quantity'] for item in
                          request.session[settings.CART_SESSION_ID].values())
    return render(request, 'operations/cart.html',
                  {'items': items, 'total_price': total_price, 'form': form, 'errors': errors})


def update_cart(request, product_id):
    errors = " "
    form = UpdateCartForm()
    if request.method == "POST":
        form = UpdateCartForm(request.POST)
        if form.is_valid():
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                messages.error(request, "You are updating product that does not exist !!!")

            if request.user.is_authenticated:
                try:
                    cart = Cart.objects.get(user=request.user, is_ordered=False)
                except Cart.DoesNotExist:
                    messages.error(request, "You don't have anything in cart")
                    return render(request, 'operations/cart.html', {'errors': errors})

                items = Items.objects.filter(cart=cart, product=product)[0]
                quantity = form.cleaned_data['quantity']
                quantity = int(quantity)

                if quantity <= product.quantity:
                    items.quantity = quantity
                    items.save()
                else:
                    messages.error(request, "You have reached the limit !!")

            else:
                product_id = str(product_id)
                quantity = form.cleaned_data['quantity']
                quantity = int(quantity)
                if quantity <= product.quantity:
                    request.session[settings.CART_SESSION_ID][product_id]['quantity'] = quantity
                    request.session.modified = True
                else:
                    messages.error("You have reached the limit !!")

            return redirect('operations:view_cart')

    return render(request, 'operations/cart.html',
                  {'form': form})


def delete_cart(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, "You are updating product that does not exist !!!")

    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user, is_ordered=False)
        except Cart.DoesNotExist:
            messages.error("You don't have anything in cart")
            return render(request, 'operations/cart.html')

        Items.objects.filter(cart=cart, product=product).delete()

    else:
        product_id = str(product_id)
        del request.session[settings.CART_SESSION_ID][product_id]
        request.session.modified = True
    return redirect('operations:view_cart')
