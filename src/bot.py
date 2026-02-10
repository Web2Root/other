import logging

from disnake import Intents
from disnake.ext.commands import InteractionBot

logging.getLogger("disnake").setLevel(logging.ERROR)
logging.getLogger("discord").setLevel(logging.ERROR)
logging.getLogger("websockets").setLevel(logging.ERROR)


class Bot(InteractionBot):
    """Class bot."""

    def __init__(self, guild_id: int) -> None:
        """Initialize the bot."""
        super().__init__(
            intents=Intents.all(),
            test_guilds=[guild_id],
        )