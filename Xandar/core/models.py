
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class Customer(AbstractUser):
    gender = models.BooleanField(default=True)
    phone_number = models.IntegerField(null=True)

    def __str__(self):
        return self.first_name
