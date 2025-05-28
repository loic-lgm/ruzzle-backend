from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.user.models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'image', 'city', 'is_staff', 'is_active', 'created_at')
    fieldsets = UserAdmin.fieldsets + (
        ("Informations supplémentaires", {"fields": ("image", "city")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Informations supplémentaires", {"fields": ("image", "city", "email")}),
    )

admin.site.register(User, CustomUserAdmin)
