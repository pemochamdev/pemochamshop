from django.contrib import admin

# Register your models here.
from category.models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date_created')
    prepopulated_fields = {"slug": ("name",)}

