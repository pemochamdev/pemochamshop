from django.shortcuts import render, get_object_or_404

# Create your views here.

from store.models import Product
from category.models import Category

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
        products = Product.objects.filter(category=category, is_available=True)
        product_count = products.count()
    
    else:
        products = Product.objects.filter(is_available=True)
        product_count = products.count()

    context = {
        'products':products,
        'categories':categories,
        'product_count':product_count,
    }

    return render(request, 'store.html', context)


def product_detail_views(request, product_slug, category_slug=None):

    try:
        single_product = Product.objects.get(slug=product_slug, category__slug=category_slug)
        
    except Exception as e:
        raise e
    
    context = {
        'single_product':single_product,
      
    }

    return render(request, 'product_detail.html', context)
