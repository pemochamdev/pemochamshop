from django.shortcuts import render, get_object_or_404, redirect


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




def cart(request):
    
    template_name = 'cart.html'
    context = {

    }

    return render(request, template_name, context)