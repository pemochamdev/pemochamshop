from django.shortcuts import render, HttpResponse, redirect
import datetime


# Create your views here.

from orders.models import Orders, OrderProduct, Payments
from orders.forms import OrdersForm
from carts.models import Cart, CartItem

def place_order(request, quantity=0, total=0):

    user_current = request.user

    # If the cart count is less than or egal to 0, then redirect back to shop 
    cart_items = CartItem.objects.filter(user=user_current)
    cart_count = cart_items.count()

    if cart_count <=0:
        return redirect('store')
   
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total +=(cart_item.product.price * cart_item.quantity)
        quantity +=cart_item.quantity
    tax = (2 * total)/100
    grand_total = tax + total

    if request.method == 'POST':
        form = OrdersForm(request.POST)

        print('request de type -> POST')

        if form.is_valid():
            # Store all the billing informations inside order table
            data = Orders()
            data.first_name = form.cleaned_data.get('first_name')
            data.last_name = form.cleaned_data.get('last_name')
            data.email = form.cleaned_data.get('email')
            data.phone = form.cleaned_data.get('phone')
            data.address_line_1 = form.cleaned_data.get('address_line_1')
            data.address_line_2 = form.cleaned_data.get('address_line_2')
            data.city = form.cleaned_data.get('city')
            data.country = form.cleaned_data.get('country')
            data.state = form.cleaned_data.get('state')
            data.order_note = form.cleaned_data.get('order_note')
            
            data.user = user_current
            data.tax = tax
            data.order_total = grand_total
            data.ip = request.META.get("REMOTE_ADDR")

            data.save()
            print('first save -> ', data)


            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            print('last save -> ', data)

            return redirect('checkout')
        else:
            return redirect("checkout")
        



    template_name = 'place-order.html'
    context = {

    }
    return render(request, context)