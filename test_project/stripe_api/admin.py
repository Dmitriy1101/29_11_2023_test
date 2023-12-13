from django.contrib import admin
from .models import Item, Order


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'currency', 'price']
    list_filter = ['id', 'name', 'price']
    list_display_links = ['name']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'total_price']
    list_filter = ['id', 'total_price']
    list_display_links = ['id']