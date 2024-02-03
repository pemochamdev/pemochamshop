from django.contrib import admin

# Register your models here.

from orders.models import Payments, Orders, OrderProduct


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_id', 'payment_method','amount_paid', 'status')


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment', 'email', 'country', 'order_total', 'tax')


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment', 'user', 'product', 'variation')

