from django.urls import path

from accounts import views

urlpatterns = [
    path("register/", views.register, name='register'),
    path("signin/", views.signin, name='signin'),
    path("logout/", views.logout_views, name='logout'),
    path("activate/<uidb64>/<token>/", views.activate, name='activate'),
    

    
]
