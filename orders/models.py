from django.db import models

# Create your models here.

from accounts.models import Account
from store.models import Product
from carts.models import Variation


class Payments(models.Model):
    user = models.ForeignKey(Account, on_delete = models.CASCADE, related_name = 'payments')
    payment_id = models.CharField(max_length = 100)
    payment_method = models.CharField(max_length = 100)
    amount_paid = models.CharField(max_length = 100) # Total amount paid
    status = models.CharField(max_length = 100)

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id
    
    class Meta:
        
        verbose_name_plural = 'Payments'


class Orders(models.Model):
    STATUS = (
        ('new', 'NEW'),
        ('accepted', 'ACCEPTED'),
        ('completed', 'COMPLETED'),
        ('cancelled', 'CANCELLED'),
    )

    user = models.ForeignKey(Account, on_delete = models.SET_NULL,null=True)
    payment= models.ForeignKey(Payments, on_delete = models.SET_NULL,null=True, blank=True)
    order_number = models.CharField(max_length = 20)
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    phone = models.CharField(max_length = 15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length = 50)
    address_line_2 = models.CharField(max_length = 50, blank=True)
    country = models.CharField(max_length = 50)
    state = models.CharField(max_length = 50)
    city = models.CharField(max_length = 50)
    order_note = models.CharField(max_length = 100, blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length = 100, choices = STATUS, default="NEW")
    ip = models.CharField(max_length = 20, blank=True)
    is_ordered = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


    def __str__(self):
        return self.user.first_name

    class Meta:
        
        verbose_name_plural = 'Orders'


class OrderProduct(models.Model):

    
    order = models.ForeignKey(Orders, on_delete = models.CASCADE)
    payment= models.ForeignKey(Payments, on_delete = models.SET_NULL,null=True, blank=True)
    user = models.ForeignKey(Account, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    variation = models.ForeignKey(Variation, on_delete = models.CASCADE)
    color = models.CharField(max_length = 50)
    size = models.CharField(max_length = 50)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


    def __str__(self):
        return self.product.name

    










    


