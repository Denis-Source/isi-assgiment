from django.conf import settings
from django.db.models import (
    Model,
    DateTimeField,
    ForeignKey,
    CASCADE,
    ManyToManyField,
    UniqueConstraint,
)
from django.utils.timezone import now


class ThreadUser(Model):
    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["thread", "user"], name="unique_participant_per_thread"
            ),
        ]

    user = ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=CASCADE, db_index=True
    )
    thread = ForeignKey("chat.Thread", on_delete=CASCADE, db_index=True)


class Thread(Model):
    participants = ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="chat.ThreadUser",
        related_name="user_threads",
    )

    updated_at = DateTimeField(
        default=now, verbose_name="Updated at", db_index=True
    )
    created_at = DateTimeField(
        default=now, verbose_name="Created at", db_index=True
    )
