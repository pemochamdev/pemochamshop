from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse


# VERIFICATION EMAIL

from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator

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

                # USER ACTIVATION
                current_site = get_current_site(request)
                mail_subject = "Please Activate Your Account "
                message = render_to_string('account_verification_email.html', {
                    'new_user': new_user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                    'token': default_token_generator.make_token(new_user)
                })

                to_email = email
                send_email = EmailMessage(mail_subject, message, to = [to_email],connection=None)
                send_email.send()


                #messages.info(request, "Registration Successful !!!")
                #messages.success(request, "Thank you for registering with us.We have sent you a 
                #verification email to your email address [mohamedpempeme7@gmail.com]. 
                #Please verify it.")
                return redirect('/accounts/signin/?command=verification&email='+email)
                
    else:

        form = AccountRegistrationForm()
    template_name = 'register.html'
    context = {
        'form': form,

    }
    return render(request, template_name, context)


def signin(request):
    
    user = request.user
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(
            email = email,
            password = password
        )

        if user is not None:
            login(request, user)
            messages.success(request, "Your Are Now Logged In !!!")
            return redirect('profile')
        else:
            messages.warning(request, 'Invalid Login CredentIals')
            return redirect('signin')
        
    
    template_name = 'signin.html'
    context = {
        #'form':form,
    }
    return render(request, template_name, context)


@login_required(login_url='signin')
def logout_views(request):
    
    logout(request)

    messages.success(request, 'Wow, You Are logged Out')

    return redirect('signin')


def activate(request, uidb64, token):

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations ! Your Account is Activated")
        return redirect('signin')
    else:
        messages.error(request, "Invalid activation link")
        return redirect('register')


@login_required(login_url = 'login')
def dashboard(request):

    context = {}
    return render(request, 'dashboard.html', context)



def forgotpassword(request):

    if request.method == 'POST':
        email = request.POST['email']

        if Account.objects.filter(email = email).exists():
            user = Account.objects.get(email__exact = email)
            
            
            # RESET PASSWORD EMAIL
            current_site = get_current_site(request)
            mail_subject = "RESET YOUR PASSWORD"
            message = render_to_string('reset_password_email.html', {
                'new_user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })

            to_email = email
            send_email = EmailMessage(mail_subject, message, to = [to_email],connection=None)
            send_email.send()


            messages.success(request, "Password reset email has been send to your email address")
            return redirect('signin')
                

        else:
            messages.error(request, 'ACCOUNT DOES NOT EXIST')
            return redirect('forgotpassword')
    

    context = {}
    return render(request, 'forgot_password.html', context)


def resetpassword_validate(request):
    return HttpResponse("resetpassword_validate")