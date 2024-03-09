from django.urls import path

from accounts import views

urlpatterns = [
    path("", views.dashboard, name='profile'),
    path("profile/", views.dashboard, name='profile'),  
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('my_orders/', views.my_orders, name='my_orders'), 
    path('order_detail/<order_id>/', views.order_detail, name= 'order_detail'),

    path("register/", views.register, name='register'),
    path("signin/", views.signin, name='signin'),
    path("logout/", views.logout_views, name='logout'),
    path("activate/<uidb64>/<token>/", views.activate, name='activate'),
    path("resetpassword_validate/<uidb64>/<token>/", views.resetpassword_validate, name='resetpassword_validate'),

    path("forgotpassword/", views.forgotpassword, name='forgotpassword'),
    path("resetpassword/", views.resetpassword, name='resetpassword'),
    path("change_password/", views.change_password, name='change_password'),
    
    
]
