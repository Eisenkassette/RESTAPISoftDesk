from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'birth_date', 'can_be_contacted', 'can_data_be_shared', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'can_be_contacted', 'can_data_be_shared')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('birth_date',)}),
        (_('Permissions'), {'fields': ('can_be_contacted', 'can_data_be_shared', 'is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'birth_date', 'password1', 'password2', 'can_be_contacted', 'can_data_be_shared'),
        }),
    )
    search_fields = ('username',)
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)