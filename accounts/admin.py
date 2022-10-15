from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from requests.models import codes
from accounts.models import User ,SMSActivation
import django.apps
from django.contrib.admin.models import LogEntry, DELETION
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django import forms
from django.forms import ModelForm 


@admin.register(User)
class AccountAdmin(UserAdmin):
    date_hierarchy = 'date_joined'
    list_display = ('full_name','phone')
    list_display_links =  ('full_name', 'phone')
    ordering = ('-date_joined',)
    filter_horizontal = 'groups','user_permissions'
    list_filter = ()
    fieldsets = ()
    add_fieldsets = (
        (None, {
            'fields': ('phone','password1', 'password2'),
        }),
    )

    def full_name(self, obj):
	    return obj.get_full_name()
 


@admin.register(SMSActivation)
class SMSActivationAdmin(admin.ModelAdmin):
    date_hierarchy = 'update'
    list_display = ('full_name','phone' ,'code','resend','activated')
    list_display_links =  ('full_name','phone' ,'code','activated')
    search_fields = ['phone']
    list_filter = ['activated']

    def full_name(self,obj):
        return obj.user.get_full_name()















