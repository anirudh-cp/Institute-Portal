from django.contrib import admin
from .models import *

from django.contrib.auth.admin import UserAdmin
from .models import account


class account_admin(UserAdmin):
    list_display = ('email','date_joined', 'last_login', 'is_admin','is_staff')
    search_fields = ('email', )
    readonly_fields=('date_joined', 'last_login')
    ordering = ('email',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('email', 'password1', 'password2'),
    }),
)


admin.site.register(account, account_admin)