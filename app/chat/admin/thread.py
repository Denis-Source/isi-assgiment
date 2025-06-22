from django.contrib.admin import ModelAdmin, register, TabularInline

from chat.models import Thread, ThreadUser


class ThreadUserInline(TabularInline):
    model = ThreadUser
    extra = 0
    autocomplete_fields = ["user"]


@register(Thread)
class ThreadAdmin(ModelAdmin):
    list_display = ["id", "updated_at", "created_at"]
    search_fields = ["participants__username"]
    autocomplete_fields = [
        "participants",
    ]
    ordering = ["-created_at"]

    inlines = [ThreadUserInline]
