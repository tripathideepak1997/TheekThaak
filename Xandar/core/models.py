
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from Xandar.util import unique_slug_generator
from .views import get_extra_field
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

ATTRIBUTE_CHOICES = [
    ('T-Shirts',
     (
         ('Shirt Size', 'Shirt Size'),
         ('Shirt Color', 'Shirt Color'),
         ('Shirt Fabric', 'Shirt Fabric')
     )),
    ('Glasses',
     (
         ('Glass Type', 'Glass Type'),
         ('Size', 'Glass Size')
     )),
    ('Shoes',
     (
         ('Shoe Type', 'Shoe Type'),
         ('Shoe Size', 'Shoe Size')
     )),
]

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)

CATEGORY_CHOICES = (
    ('Electronics', 'Electronics'),
    ('Clothing', 'Clothing'),
    ('Lifestyle', 'Lifestyle'),
)


SUB_CATEGORY_CHOICES = (
    ('T-Shirts', 'T-Shirts'),
    ('Glasses', 'Glasses'),
    ('Shoes', 'Shoes'),
)


class Customer(AbstractUser):
    gender = models.BooleanField(default=True)
    phone_number = models.IntegerField(null=True)

    def __str__(self):
        if self.first_name == '':
            return 'No Name Specified'
        else:
            return self.first_name


class Product(models.Model):
    name = models.CharField(max_length=50, blank=False)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    description = models.CharField(max_length=255)
    price = models.PositiveIntegerField(blank=False)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20)
    sub_category = models.CharField(choices=SUB_CATEGORY_CHOICES, max_length=20)
    quantity = models.PositiveIntegerField(default=1)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10)
    replacement = models.IntegerField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self)
        super(Product, self).save(*args, **kwargs)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, parent_link=True)
    image = models.FileField(upload_to='product_images/', default='product_images/default.jpg')


class ExtraAttribute(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.CharField(max_length=50)
    value = models.CharField(max_length=50)


class Attribute(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.CharField(max_length=50, choices=get_extra_field(ExtraAttribute, ATTRIBUTE_CHOICES), default='Default')
    value = models.CharField(max_length=50)


class Wishlist(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_image = models.ForeignKey(ProductImage, on_delete=models.CASCADE)


    def __str__(self):
        return self.product.name

    def get_absolute_url(self):
        return reverse('operations:wishlist')

#-------------PREVIOUS WORK - WEEK ONE---------------#
class OrderedItems(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_image = models.ForeignKey(ProductImage, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)

class DeliveryAddresses(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    receiver_name = models.CharField(max_length=50, blank=False)
    street_address = models.CharField(max_length=50, blank=False)
    city = models.CharField(max_length=50, blank=False)
    pincode = models.IntegerField(blank=False)
    state = models.CharField(max_length=50, blank=False)
    phone_number = models.IntegerField(blank=False)


# Defining Validators



def validate_quantity(value):
    if value not in range(1, 4):
        raise ValidationError(
            _('Product cannot be more than 3 '),
            params={'value': value},
        )


class Cart(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    is_ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name


class Items(models.Model):
    choices = [(i, str(i)) for i in range(1, 4)]
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    product_img = models.OneToOneField(ProductImage, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(validators=[validate_quantity, ], choices=choices)
    unit_price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name=_('unit price'))

    def __str__(self):
        return self.product.name




