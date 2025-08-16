from django.contrib import admin
from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "get_participants", "updated")
    ordering = ("-updated",)
    search_fields = ("participants__username",)

    def get_participants(self, obj):
        return ", ".join([user.username for user in obj.participants.all()])

    get_participants.short_description = "Participants"


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "conversation",
        "user",
        "short_content",
        "created",
        "is_read",
    )
    list_filter = ("is_read", "created")
    search_fields = ("content", "user__username", "conversation__id")
    ordering = ("-created",)

    def short_content(self, obj):
        return obj.content[:50] + ("..." if len(obj.content) > 50 else "")

    short_content.short_description = "Content"
