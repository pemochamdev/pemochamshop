from django.urls import path

from accounts import views

urlpatterns = [
    path(" ", views.dashboard, name='profile'),
    path("profile/", views.dashboard, name='profile'),        

    path("register/", views.register, name='register'),
    path("signin/", views.signin, name='signin'),
    path("logout/", views.logout_views, name='logout'),
    path("activate/<uidb64>/<token>/", views.activate, name='activate'),
    path("resetpassword_validate/<uidb64>/<token>/", views.resetpassword_validate, name='resetpassword_validate'),

    path("forgotpassword/", views.forgotpassword, name='forgotpassword')
    
    
]
