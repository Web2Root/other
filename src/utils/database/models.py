from tortoise import fields
from tortoise.models import Model


class Ticket(Model):
    """Model Ticket."""

    discord_id = fields.BigIntField(unique=True)
    channel_id = fields.BigIntField(unique=True)
    category_id = fields.BigIntField(unique=True)

    class Meta:
        """Meta."""

        table = "tickets"


class Votes(Model):
    """Model Votes."""

    votes_id = fields.BigIntField(pk=True)
    likes = fields.JSONField(default=[])
    dislikes = fields.JSONField(default=[])

    class Meta:
        """Meta."""

        table = "votes"
