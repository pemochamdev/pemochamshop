from django.contrib import admin

# Register your models here.

from store.models import Product, ReviewRating, ProductGallery

class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra =1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'stock','category','is_available', 'created_at', 'updated_at']
    prepopulated_fields = {"slug": ("name",)}
    list_display_links = ['name']
    inlines = [ProductGalleryInline]


@admin.register(ReviewRating)
class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'subject', 'rating', 'created_at', 'updated_at')

admin.site.register(ProductGallery)