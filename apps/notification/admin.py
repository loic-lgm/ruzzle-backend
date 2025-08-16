from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "notif_type",
        "is_read",
        "created_at",
    )
    list_filter = ("notif_type", "is_read", "created_at")
    search_fields = ("user__username",)
    ordering = ("-created_at",)
