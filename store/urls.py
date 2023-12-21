from django.urls import path

from store import views

urlpatterns = [
    path('', views.home, name='home'),
    path('store/', views.store, name='store'),
    path('store/<category_slug>/<product_slug>/', views.product_detail_views, name='product_detail'),
    path('store/<category_slug>/', views.store, name='product_by_category'),
]
