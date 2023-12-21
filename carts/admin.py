from django.contrib import admin

# Register your models here.

from carts.models import Cart, CartItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id','cart_id', 'date_add']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'product','cart', 'quantity', 'is_active']

