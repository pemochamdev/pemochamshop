from django.db import models
from django.urls import reverse
from django.db.models import Avg, Count

# Create your models here.

from category.models import Category
from accounts.models import Account

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
    


    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg


    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count
    
    

class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    user = models.ForeignKey(Account, on_delete = models.CASCADE)
    subject  = models.CharField(max_length=200, blank=True)
    review  = models.TextField(max_length=500)
    rating  = models.FloatField()
    ip  = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
    


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    image = models.ImageField(upload_to='store/products',max_length=255)

    def __str__(self):
        return self.product.name
    

    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'
    