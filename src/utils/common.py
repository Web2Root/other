from __future__ import annotations

from json import dump, load
from pathlib import Path
from typing import TYPE_CHECKING

from src.utils.logging import log

if TYPE_CHECKING:
    from disnake.ext import commands


class Common:
    """Class common."""

    def read_json(self, path: str, *keys: str) -> dict | list:
        """Read Json File."""
        file_path = Path(path)

        with file_path.open("r", encoding="utf-8") as file:
            data = load(file)

        for key in keys:
            data = data.get(str(key))
            if data is None:
                return None

        return data

    def write_json(self, path: str, data: dict | list) -> None:
        """Write Json File."""
        file_path = Path(path)

        with file_path.open("w", encoding="utf-8") as file:
            dump(data, file, ensure_ascii=False, indent=4)

    def load_cogs(self, bot: commands.Bot) -> None:
        """Load cogs."""
        for folder in (Path.cwd() / "src").iterdir():
            if not folder.is_dir() or folder.name == "utils":
                continue

            for file in folder.glob("*.py"):
                bot.load_extension(f"src.{folder.name}.{file.stem}")

        log.info("Cogs successfully loaded")


commons = Common()
