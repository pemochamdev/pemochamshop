from django.urls import path

from store import views

urlpatterns = [
    path('', views.home, name='home'),
    path('store/', views.store, name='store'),    
    path('store/search/', views.search, name='search'),
    path('store/<category_slug>/<product_slug>/', views.product_detail_views, name='product_detail'),
    path('store/<category_slug>/', views.store, name='product_by_category'),
    path("submit_review/<product_id>/", views.submit_review, name='submit_review'),
]
