from django.urls import path

from category import views

urlpatterns = [
    path('', views.home, name='home'),
]
