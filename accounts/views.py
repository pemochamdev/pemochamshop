from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect, get_object_or_404

#Other import
from orders.models import Orders

# Request
import requests


# VERIFICATION EMAIL

from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from carts.views import _cart_id
from carts.models import Cart, CartItem
from accounts.models import Account, UserProfile
from accounts.forms import AccountRegistrationForm, UserForm, UserProfileForm

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

                return redirect('/accounts/signin/?command=verification&email='+email)
                
    else:

        form = AccountRegistrationForm()
    template_name = 'register.html'
    context = {
        'form': form,

    }
    return render(request, template_name, context)


def signin(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(
            email = email,
            password = password
        )


        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()

                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    
                    # Getting the product variation by cart id
                    product_variation = []
                    for item in cart_item:
                        variations = item.variations.all()
                        product_variation.append(list(variations))
                 
                    # Get Cart Item from user to access is product variation
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    
                    #IF THE CURRENT VARIATION IS INSIDE THE EXISTING VARIATION increase qty of the item
                    
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)
                    
                    for prd_variation in product_variation:
                        if prd_variation in ex_var_list:
                            index = ex_var_list.index(prd_variation)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            item = CartItem.objects.create(cart=cart)
                            for item in cart_item:
                                item.user = user
                        
                                item.save()
                    


            except:
                pass
            login(request, user)
            messages.success(request, "Your Are Now Logged In !!!")
            url = request.META.get("HTTP_REFERER")
            try:
                query = requests.utils.urlparse(url).query
                print('query --> ', query)
                params = dict(x.split("=") for x in query.split("&"))
                print('params --> ', params)
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('profile')
                
        else:
            messages.warning(request, 'Invalid Login CredentIals')
            return redirect('signin')
        
    
    template_name = 'signin.html'
    context = {
        #'user':user,
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

    orders = Orders.objects.filter(user_id = request.user.id, is_ordered = True).order_by('created_at')
    orders_count = orders.count()

    context = {
        'orders':orders,
        'orders_count':orders_count
    }
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


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        user.save()
        messages.success(request, "Please reset your pasword !")
        return redirect('resetpassword')
    else:
        messages.error(request, "This link  has been expired")
        return redirect('signin')


def resetpassword(request):

    template_names = 'resetpassword.html'

    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password Reset Successful')
            return redirect('signin')

        else:
            messages.error(request, "Passwod does not match")
            return redirect('resetpassword')
    else:


        return render(request,template_names)



def my_orders(request):
    user = request.user
    orders = Orders.objects.filter(user=user, is_ordered=True).order_by('-created_at')
    

    context = {
        'orders':orders,
    }

    return render(request, 'my_orders.html', context)


@login_required(login_url='login')
def edit_profile(request):
    user = request.user
    userprofile = get_object_or_404(UserProfile, user=user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance = user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }

    return render(request, 'edit_profile.html', context)