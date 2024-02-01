from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.
from store.models import Product
from carts.models import Cart, CartItem, Variation


def _cart_id(request):
    cart  = request.session.session_key

    if not cart:
        cart  = request.session.create()
    return cart


# def add_cart(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     product_variation = []

#     if request.method == 'POST':
#         for item in request.POST:
#             key = item
#             value = request.POST[key]
#             # print("key:", key)
#             # print("value:", value)
#             try:

#                 # variation = Variation.objects.get(
#                 #     product = product,
#                 #     variation_category__iexact=key,
#                 #     variation_value__iexact=value
#                 # )
#                 variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
#                 product_variation.append(variation)
#                 print(variation)
#             except:
#                 pass

#     #     color = request.POST.get('color')
#     #     size = request.POST.get('size')
#     # print(color)
#     # print(size)

#     try:
#         cart = Cart.objects.get(cart_id=_cart_id(request)) 
        
#     except Cart.DoesNotExist:
#         cart = Cart.objects.create(cart_id=_cart_id(request)) 
#     cart.save()


#     is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()

#     if is_cart_item_exists:
#         cart_item = CartItem.objects.filter(product=product, cart=cart)
#         # existing_variation ---> database
#         # current variation ---> product_variation
#         # item_id ---> database
        
#         existing_variation_list = []
#         ex_var_list = []
#         id = []
#         for item in cart_item:
#             existing_variation = item.variations.all()
#             ex_var_list.append(list(existing_variation))
#             id.append(item.id)

#         print(ex_var_list)

#         #print(existing_variation_list)

#         #print("cart_item",cart_item)
#         if product_variation in existing_variation:
#             # return HttpResponse("Vrai")
#             # increase the cart item quantity
#                # increase the cart item quantity
#             index = ex_var_list.index(product_variation)
#             item_id = id[index]
#             item = CartItem.objects.get(product=product, id=item_id)
#             item.quantity += 1
#             item.save()
#         else:
#             # return HttpResponse("Faux")
#             item = CartItem.objects.create(product=product,  quantity=1,cart=cart)

#             print("cart_item",cart_item)
#             # create a new cart item
#             if len(product_variation)>0:
#                 item.variations.clear()
#                 item.variations.add(*product_variation)
                
#                 # for item in product_variation:
#                 #     cart_item.variations.add(item)

#             # cart_item.quantity += 1
#             item.save()

#     else :
#         cart_item = CartItem.objects.create(
#             product=product,
#             cart=cart,
#             quantity = 1,
#         )
#         if len(product_variation)>0:
#             cart_item.variations.clear()
#             for item in product_variation:
#                 cart_item.variations.add(item)

#         cart_item.save()

#     return redirect('cart')



#@login_required(login_url='signin')
def add_cart(request, product_id):
  product = Product.objects.get(id=product_id)#get product
  product_variation = []
  if request.method == 'POST':
    #loop tru variations(color and size)
    for item in request.POST:
      key = item
      value = request.POST[key]
      # check if key and value matches Variation Model methods (color and size)
      try:
        variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
        product_variation.append(variation)
      except:
        pass

  #if cart exists get the card in session else create cart object
  try:
    cart = Cart.objects.get(cart_id=_cart_id(request)) #get the cart using the cart_id present in the session
  except Cart.DoesNotExist:
    cart = Cart.objects.create(
      cart_id=_cart_id(request)
    )
  cart.save()

  # Check if cart item exists or not:
  is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()

  # if cartItem already available in the cart/cart session
  # cart with product and add cart qty
  if is_cart_item_exists:
    cart_item = CartItem.objects.filter(product=product, cart=cart)
    # existing variations -> database
    # current variation -> product_variation
    # item id -> database
    ex_var_list = []
    id = []
    #IF THE CURRENT VARIATION IS INSIDE THE EXISTING VARIATION increase qty of the item
    for item in cart_item:
      existing_variation = item.variations.all()
      ex_var_list.append(list(existing_variation))
      id.append(item.id)
    print(ex_var_list)
    if product_variation in ex_var_list:
      # increase the cart item quantity
      index = ex_var_list.index(product_variation)
      item_id = id[index]
      item = CartItem.objects.get(product=product, id=item_id)
      item.quantity += 1
      item.save()
    else:
      #create new cart item
      item = CartItem.objects.create(product=product, quantity=1, cart=cart)
      # add variation in the cart item
      if len(product_variation) > 0:
        item.variations.clear()
        item.variations.add(*product_variation)
      item.save()
  else:
    #if cartitem not exist create new cart item
    cart_item = CartItem.objects.create(
      product=product,
      quantity=1,
      cart=cart,
    )
    # add variation in the cart item
    if len(product_variation) > 0:
      cart_item.variations.clear()
      cart_item.variations.add(*product_variation)
    cart.save()
  return redirect('cart')



@login_required(login_url='signin')
def remove_cart(request,product_id, cart_item_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = get_object_or_404(CartItem, product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity >1:

            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
       pass
    return redirect('cart')


@login_required(login_url='signin')
def remove_cart_item(request,product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
       
        cart_item = get_object_or_404(CartItem, product=product, cart=cart, id=cart_item_id)
        cart_item.delete()
    except:
       pass
    return redirect('cart')



@login_required(login_url='signin')
def cart(request, quantity=0, cart_items=None,total=0):
  
  
  try:
    tax = 0
    grand_total = 0
    if request.user.is_authenticated:
       
      cart_items = CartItem.objects.filter(user=request.user, is_active = True)
    else:

      cart = Cart.objects.get(cart_id=_cart_id(request))
      cart_items = CartItem.objects.filter(cart=cart, is_active = True)
    for cart_item in cart_items:
        total +=(cart_item.product.price*cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = tax + total
  except ObjectDoesNotExist :
    pass


  template_name = 'cart.html'  
  context = {
        'cart_items':cart_items,
        'total':total,
        'quantity':quantity,
        'tax':tax,
        'grand_total':grand_total,
    }
  return render(request, template_name, context)



@login_required(login_url='signin')
def checkout(request,  quantity=0, cart_items=None,total=0):

  try:
    tax = 0
    grand_total = 0
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart)
    for cart_item in cart_items:
        total +=(cart_item.product.price*cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = tax + total
  except ObjectDoesNotExist :
    pass


  context = {
    'cart_items':cart_items,
    'total':total,
    'quantity':quantity,
    'tax':tax,
    'grand_total':grand_total,
    }
   
  return render(request, 'checkout.html', context)