from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
from store.models import Product
from carts.models import Cart, CartItem

def _cart_id(request):
    cart  = request.session.session_key

    if not cart:
        cart  = request.session.create()
    return cart


def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request)) 
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()

    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity = 1,
        )
    cart_item.save()

    return redirect('cart')




def cart(request, quantity=0, cart_items=None,total=0):
    try:
        cart = Cart.object.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart)
        for cart_item in cart_items:
            total +=(cart_item.product.price*cart_item.quantity)
            quantity += cart_item.quantity
    except ObjectDoesNotExist :
        pass


    template_name = 'cart.html'
    context = {
        'cart_items':cart_items,
        'total':total,
        'quantity':quantity,
    }

    return render(request, template_name, context)