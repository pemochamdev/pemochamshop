from django.db import models
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description  = models.TextField()
    image = models.ImageField(upload_to='photos/category')

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

    def get_absolute_url(self):
        return reverse("category", kwargs={"slug": self.slug})
    
    