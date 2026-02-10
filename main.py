import asyncio

from src.bot import Bot
from src.utils import commons, db, log, settings


async def main() -> None:
    """Start bot function."""
    try:
        bot = Bot(settings.bot.guild)
        commons.load_cogs(bot)

        await db.connect()
        await bot.start(settings.bot.token)
    finally:
        await db.disconnect()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("Program interrupted")
