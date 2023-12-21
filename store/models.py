from django.db import models
from django.urls import reverse

# Create your models here.

from category.models import Category

class Product(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description  = models.TextField(max_length=500)
    image = models.ImageField(upload_to='photos/products')
    price = models.IntegerField(default=0)
    discount_price = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"product_slug": self.slug, "category_slug":self.category.slug})
    
    

