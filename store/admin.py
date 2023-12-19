from django.contrib import admin

# Register your models here.

from store.models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'stock','category','is_available', 'created_at', 'updated_at']
    prepopulated_fields = {"slug": ("name",)}
    list_display_links = ['name']


