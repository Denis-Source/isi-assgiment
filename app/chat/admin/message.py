from django.contrib.admin import ModelAdmin, register

from chat.models import Message


@register(Message)
class MessageAdmin(ModelAdmin):
    list_display = ["id", "is_read", "thread", "sender", "text", "created_at"]
    search_fields = ["text", "sender__username"]
    autocomplete_fields = ["sender", "thread"]
    ordering = ["-created_at"]
