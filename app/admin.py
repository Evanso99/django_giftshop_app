from django.contrib import admin
from app.models import Product
from . models import *

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Cartitems)
admin.site.register(ShippingAddress)
