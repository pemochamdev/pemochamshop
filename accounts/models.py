from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, last_name, first_name, email,username, password=None):
        if not email:
            raise ValueError('User most have an email address')
        if not username:
            raise ValueError('User most have an username')
        
        user = self.model(
            email = self.normalize_email(email),
            last_name = last_name,
            first_name = first_name,
            username=username
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, last_name, first_name, email,username, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            last_name=last_name,
            first_name=first_name,
            password=password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superadmin = True
        user.is_actif = True
        user.save(using = self._db)
        return user

    

class Account(AbstractBaseUser):

    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    username = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    phone_numbre = models.CharField(max_length=120)

    # required

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['username','first_name', 'last_name']

    objects = MyAccountManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'


    def __str__(self):
        return self.email
    

    def has_perm(self,  perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True
    

    


class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    address_line_1 = models.CharField(blank=True, max_length=100)
    address_line_2 = models.CharField(blank=True, max_length=100)
    profile_picture = models.ImageField(blank=True, upload_to='userprofile')
    city = models.CharField(blank=True, max_length=20)
    state = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)

    def __str__(self):
        return self.user.first_name

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'