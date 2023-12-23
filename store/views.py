from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

# Create your views here.

from store.models import Product
from category.models import Category
from carts.models import Cart, CartItem
from carts.views import _cart_id

def home(request):
    products = Product.objects.filter(is_available=True).order_by('-created_at')

    context = {
        'products':products,
    }

    return render(request, 'index.html', context)


def store(request, category_slug=None):
    category=None
    products=None
    
    categories = Category.objects.all()
    if category_slug != None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True).order_by('-created_at')
        paginator = Paginator(products, 1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    
    else:
        products = Product.objects.filter(is_available=True).order_by('-created_at')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        'products':paged_products,
        'categories':categories,
        'product_count':product_count,
        'paged_products':paged_products,
    }

    return render(request, 'store.html', context)


def product_detail_views(request, product_slug, category_slug=None):

    try:
        single_product = Product.objects.get(slug=product_slug, category__slug=category_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
        
    except Exception as e:
        raise e
    
    context = {
        'single_product':single_product,
        'in_cart':in_cart,
      
    }

    return render(request, 'product_detail.html', context)


def search(request):
    categories = Category.objects.all()

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.filter(Q(description__icontains=keyword) |Q(name__icontains=keyword ) ).order_by('created_at')
            product_count = products.count()

    
    context = {
        'products':products,
        'product_count':product_count,
        'categories':categories,

    }
    return render(request, 'store.html', context)
    