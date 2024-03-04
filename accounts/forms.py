from typing import Any
from django import forms 

from accounts.models import Account,UserProfile


class AccountRegistrationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        #'placeholder':'Enter your password here',
        #'class':'form-control'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        #'placeholder':'Repeat your same password here',
        #'class':'form-control'
    }))
    
    class Meta:
        model = Account
        fields = ("first_name", "last_name", "email", "phone_numbre", "password")
    

    def clean(self):
        cleaned_data = super(AccountRegistrationForm, self).clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        
        if password != confirm_password:
            forms.ValidationError("password does not match")
     


    def __init__(self, *args, **kwargs):
        super(AccountRegistrationForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter Your First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Your Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Your Email'
        self.fields['phone_numbre'].widget.attrs['placeholder'] = 'Enter Your Phone Number'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
    


class SigninForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        
    }))

    class Meta:
        model = Account
        fields = ('email', 'password')
    

    def clean(self) :
        cleaned_data = super(SigninForm, self).clean()

        password = cleaned_data.get('password')

        return super().clean()
    

    def __init__(self, *args, **kwargs):
        super(SigninForm, self).__init__(*args, **kwargs)

        self.fields['password'].widget.attrs['placeholder'] = 'Enter Your First Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Your Email'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_numbre')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ('address_line_1', 'address_line_2', 'city', 'state', 'country', 'profile_picture')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'