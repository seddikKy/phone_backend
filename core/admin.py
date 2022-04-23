# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea

from core.models import Tier, Contact, Role, CallLog, NewUser, Position


class UserAdminConfig(UserAdmin):
    """
        Custom user admin
    """
    model = NewUser
    search_fields = ('email', 'user_name', 'first_name',)
    list_filter = ('email', 'user_name', 'first_name', 'is_active', 'is_staff')
    ordering = ('-start_date',)
    list_display = ('email', 'user_name', 'first_name', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'first_name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff',)}),
        ('Personal', {'fields': ('about',)}),
    )

    formfield_overrides = {
        NewUser.about: {"widget": Textarea(attrs={'rows': 10, 'cols': 40})},
    }

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'first_name', 'password1', 'password2', 'is_active', 'is_staff')
        }
         ),
    )


admin.site.register(Tier)
admin.site.register(Contact)
admin.site.register(Role)
admin.site.register(CallLog)
admin.site.register(Position)
admin.site.register(NewUser, UserAdminConfig)
