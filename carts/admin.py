from django.contrib import admin

# Register your models here.

from carts.models import Cart, CartItem, Variation

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id','cart_id', 'date_add']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'product','cart', 'quantity', 'is_active']


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'variation_category', 'variation_value', 'is_active', 'created_date']
    list_editable = ['is_active',]
    search_fields = ('variation_category','variation_value')
    list_filter = ('product', 'variation_category','variation_value')
