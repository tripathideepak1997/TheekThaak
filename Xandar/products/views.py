from django.shortcuts import render
from django.views.generic.list import ListView
from core.models import Product, ProductImage, Attribute, ExtraAttribute
from django.db.models import Q
from operations.views import add_to_cart






class ProductListView(ListView):
	model = Product
	template_name = "products/product_list.html"
	paginate_by = 3


	def get_queryset(self, *args, **kwargs):
		qs = Product.objects.all()
		query = self.request.GET.get("category", None)
		if query is not None:
			qs = qs.filter(Q(category__icontains=query) |
    			Q(sub_category__icontains=query)
    			)

		return qs


	def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
		context = super().get_context_data(**kwargs)
		context['image']=[]

        # Add in a QuerySet of all the books
		# for object in context['object_list']:
		# 	object.image = Product.objects.filter(name=object.name).main_image
		# print(context['image'])
		for object in context['object_list']:
			#print(object.main_image)
			print(object)
			object.image = ProductImage.objects.filter(product = object).first().image
		return context



		# [{a,b,c,d},{a,b,c},{a,b,c}]






















































#Aman
from django.views.generic import DetailView
#from operations.cart import add_cart
from operations.views import add_wishlist_item
from django.http import HttpResponse
from core.models import Wishlist

class ProductDetailView(DetailView):
	model = Product
	template_name = 'products/product_detail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['attributes'] = []
		context['images'] = []
		for attributes in Attribute.objects.filter(product_id=context['object']):
			context['attributes'].append(attributes)
		for attributes in ExtraAttribute.objects.filter(product_id=context['object']):
			context['attributes'].append(attributes)
		for image in ProductImage.objects.filter(product_id=context['object']):
			context['images'].append(image)
		return context


def product_add_wishlist_cart(request, pk):
	action_perfomed = request.GET.get('button')
	quantity = int(request.GET.get('quantity'))
	if action_perfomed == 'wishlist':
		return HttpResponse(add_wishlist_item(request, pk))
	else:
		return HttpResponse(add_to_cart(request, pk, quantity))





































































#Amulya



































































































#Deepak