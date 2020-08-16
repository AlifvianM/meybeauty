from django.contrib import admin
from . import models
# Register your models here.
from .models import Product, OrderItem, Order, Pembayaran, Member, Reseller



admin.site.register(models.Product)
admin.site.register(models.OrderItem)
admin.site.register(models.Order)
admin.site.register(Pembayaran)
admin.site.register(Member)
admin.site.register(Reseller)