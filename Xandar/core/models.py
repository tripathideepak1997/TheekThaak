
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from .views import get_extra_field



class Customer(AbstractUser):
    gender = models.BooleanField(default=True)
    phone_number = models.IntegerField(null=True)

    def __str__(self):
        return self.first_name

ATTRIBUTE_CHOICES = [
    ('T-Shirts',
     (
         ('shirt_size', 'Shirt Size'),
         ('shirt_color', 'Shirt Color'),
         ('shirt_fabric', 'Shirt Fabric')
     )),
    ('Glasses',
     (
         ('glass_type', 'Glass Type'),
         ('glass_size', 'Glass Size')
     )),
    ('Shoes',
     (
         ('shoe_type','Shoe Type'),
         ('shoe_size', 'Shoe Size')
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


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20)
    sub_category = models.CharField(choices=SUB_CATEGORY_CHOICES, max_length=20)
    quantity = models.IntegerField(default=0)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10)
    replacement = models.IntegerField()












class ExtraAttribute(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.CharField(max_length=50, unique=True)
    value = models.CharField(max_length=50)












class Attribute(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.CharField(max_length=50, choices=get_extra_field(ExtraAttribute, ATTRIBUTE_CHOICES), default='Default')
    value = models.CharField(max_length=50)












class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_image = models.FileField(upload_to='product_images/', default='product_images/default.jpg')









