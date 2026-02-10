from tortoise import Tortoise

from src.utils.config import settings


class Database:
    """Class connect database."""

    def __init__(self, config: dict) -> None:
        """Init database."""
        self.config = config

    async def connect(self) -> None:
        """Connect database."""
        await Tortoise.init(config=self.config)
        await Tortoise.generate_schemas()

    async def disconnect(self) -> None:
        """Close database."""
        await Tortoise.close_connections()


db = Database(config=settings.database.config)
