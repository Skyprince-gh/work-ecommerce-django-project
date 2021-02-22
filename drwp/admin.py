from django.contrib import admin
from .models import StoreCategory, Restaurant, Menu, Item, OrderItem, Order

admin.site.register(StoreCategory)
admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
