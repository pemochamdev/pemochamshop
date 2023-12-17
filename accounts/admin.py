from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from accounts.models import Account


class AccountAdmin(UserAdmin):
    list_display = ['id', 'email', 'username', 'first_name', 'date_joined']
    list_display_links = ['email', 'username', 'first_name']
    readonly_fields = ['last_login', 'date_joined']
    ordering =['-date_joined']


    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)