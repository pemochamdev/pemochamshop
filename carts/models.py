from django.db import models

# Create your models here.
import uuid
from store.models import Product

class Cart(models.Model):
    
    cart_id = models.CharField(max_length=200, unique=True, editable=False)
    date_add = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.cart_id)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart')
    quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product.name

    def sub_total(self):
        return self.product.price*self.quantity


class Variation(models.Model):
    variation_category_choices =(
        ('color', 'color'),
        ('size', 'size'),
    )
    # variation_value_choices = (
    #     ()
    # )
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    variation_category = models.CharField(max_length=200, choices = variation_category_choices)
    variation_value = models.CharField(max_length=200)#, choices = variation_value_choices
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.product.name
    