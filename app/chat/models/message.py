from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.db.models import (
    Model,
    BooleanField,
    TextField,
    ForeignKey,
    CASCADE,
    DateTimeField,
)
from django.utils.timezone import now


class Message(Model):
    class Meta:
        indexes = [
            GinIndex(
                fields=["text"],
                name="text_trgm_idx",
                opclasses=["gin_trgm_ops"],
            ),
        ]

    is_read = BooleanField(default=False)
    text = TextField()
    sender = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name="user_messages",
    )
    thread = ForeignKey("chat.Thread", on_delete=CASCADE, db_index=True)

    created_at = DateTimeField(
        default=now, verbose_name="Created at", db_index=True
    )
