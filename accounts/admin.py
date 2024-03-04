from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from accounts.models import Account, UserProfile


class AccountAdmin(UserAdmin):
    list_display = ['id', 'email', 'username', 'first_name', 'date_joined']
    list_display_links = ['email', 'username', 'first_name']
    readonly_fields = ['last_login', 'date_joined']
    ordering =['-date_joined']


    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()



class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_picture.url))
    thumbnail.short_description = 'Profile Picture'
    list_display = ('thumbnail', 'user', 'city', 'state', 'country')


admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
