from django.db import models
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.conf import settings
from django.db.models.lookups import IntegerFieldFloatRounding
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    security_question = models.CharField(max_length=100)
    groups = models.ManyToManyField(
        Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name='customuser_set', blank=True)



class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', default='default_product_image.jpg', null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    product_code = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.name


    
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    cart_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    completed = models.BooleanField(default=False)
    



    @property
    def get_cart_total(self):
        cartitems = self.cartitems_set.all()
        total = sum([item.product.price * item.quantity for item in cartitems])
        return total
    
    @property
    def get_itemtotal(self):
        cartitems = self.cartitems_set.all()
        total = sum([item.quantity for item in cartitems])
        return total

    def __str__(self):
        return str(self.id)



class Cartitems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE )
    product =  models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)


    @property
    def get_total(self):
        total = self.quantity * self.product.price
        if total == 0.00:
            self.delete()
        return total

    

    def __str__(self):
        return self.product.name

class ShippingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)

    def __str__(self):
        return self.address

