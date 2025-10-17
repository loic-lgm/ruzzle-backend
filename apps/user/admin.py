from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.user.models import User


class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "image",
        "city",
        "latitude",
        "longitude",
        "postal_code",
        "city_name",
        "is_staff",
        "is_active",
        "created_at",
    )
    fieldsets = UserAdmin.fieldsets + (
        (
            "Informations supplémentaires",
            {
                "fields": (
                    "image",
                    "city",
                    "latitude",
                    "longitude",
                    "postal_code",
                    "city_name",
                )
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Informations supplémentaires",
            {
                "fields": (
                    "image",
                    "city",
                    "latitude",
                    "longitude",
                    "postal_code",
                    "city_name",
                    "email",
                )
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
