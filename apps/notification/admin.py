from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "notif_type",
        "short_content",
        "is_read",
        "created_at",
    )
    list_filter = ("notif_type", "is_read", "created_at")
    search_fields = ("user__username", "content")
    ordering = ("-created_at",)

    def short_content(self, obj):
        return obj.content[:50] + ("..." if len(obj.content) > 50 else "")

    short_content.short_description = "Content"
