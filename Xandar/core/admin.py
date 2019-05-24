from django.contrib import admin
#from core.models import Customer, Attribute, Product, ExtraAttribute, ProductImage
from core.models import *
from django.contrib.auth.admin import UserAdmin

class ProductImageInline(admin.StackedInline):
    model = ProductImage
    initial_num = 1

    def get_extra(self, request, obj=None, **kwargs):
         return self.initial_num


class ExtraAttributeInline(admin.TabularInline):
    model = ExtraAttribute
    initial_num = 1

    def get_extra(self, request, obj=None, **kwargs):
        return self.initial_num


class AttributeInline(admin.TabularInline):
    model = Attribute
    initial_num = 0

    def get_extra(self, request, obj=None, **kwargs):
        return self.initial_num

class ProductAdmin(admin.ModelAdmin):
    ordering = ('sub_category',)
    search_fields = ['gender', 'category', 'sub_category', 'name']
    list_display = ('name', 'category', 'sub_category', 'gender')
    list_filter = ('category','sub_category','gender')
    inlines = [
        ProductImageInline, AttributeInline, ExtraAttributeInline
    ]

class CustomerAdmin(UserAdmin):
    #fields = ('username','first_name','last_name','email','last_login', 'phone_number')
    list_display = ('first_name', 'last_name', 'username','email')
    list_filter = ('first_name','email')
    search_fields = ['first_name','email','username']

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
# admin.site.register(ExtraAttribute)