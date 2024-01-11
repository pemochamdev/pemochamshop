from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages

from accounts.forms import AccountRegistrationForm
from accounts.models import Account


# Create your views here.


def register(request):
    
    if request.method == "POST":
        form = AccountRegistrationForm(request.POST)

        if form.is_valid():
            
            last_name = form.cleaned_data['last_name']
            first_name = form.cleaned_data['first_name']
            email = form.cleaned_data['email']
            phone_numbre = form.cleaned_data['phone_numbre']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            # Creation automatique du username
            username = email.split("@")[0]

            if password != confirm_password:
                
                messages.info(request, "password does not match")
                
            else:

                new_user = Account.objects.create_user(
                    last_name = last_name,
                    first_name = first_name,
                    email = email,                    
                    password = password,
                    username = username,
                )
                new_user.phone_numbre = phone_numbre
                new_user.save()
                return redirect('signin')
                
    else:

        form = AccountRegistrationForm()
    template_name = 'register.html'
    context = {
        'form': form,

    }
    return render(request, template_name, context)


def signin(request):
    
    user = request.user
    
    
    template_name = 'signin.html'
    context = {

    }
    return render(request, template_name, context)



def logout_views(request):
    
    logout(request)
    return redirect('home')

