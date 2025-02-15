from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import User

class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'image', 'is_staff', 'is_active', 'created_at')

admin.site.register(User, UserAdmin)