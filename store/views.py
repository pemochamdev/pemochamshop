from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

from carts.views import _cart_id
from category.models import Category
from carts.models import Cart, CartItem
from orders.models import OrderProduct
from store.forms import ReviewRatingForm
from store.models import Product, ReviewRating,ProductGallery


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
    if request.user.is_authenticated:

        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id = single_product.id).exists()

        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = OrderProduct.objects.filter(product_id = single_product.id).exists()

    # Get the reviews
    reviews = ReviewRating.objects.filter(product_id = single_product.id, status=True)


    # Get Product gallery
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    context = {
        'single_product':single_product,
        'in_cart':in_cart,
        'orderproduct':orderproduct,
        'reviews':reviews,
        'product_gallery':product_gallery,
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



def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewRatingForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewRatingForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)

