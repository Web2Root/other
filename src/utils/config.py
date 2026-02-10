from typing import Any, Literal

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class BotConfig(BaseModel):
    """Bot config model."""

    token: str
    guild: int
    panel_cmd: dict[str, str] = {
        "📬 Система тикет": "ticket",
        "📍 Система обратной связи": "feedback",
    }


class ColorConfig(BaseModel):
    """Color config."""

    red: int = 16711680
    green: int = 65280
    blue: int = 255
    yellow: int = 16776960
    purple: int = 9109759
    default: int = 3750465


class EmojiConfig(BaseModel):
    """Класс с emoji."""

    like: str = "<a:_:1158181671720464485>"
    dislike: str = "<a:_:1158181826624487485>"


class LoggingConfig(BaseModel):
    """Logging config model."""

    log_format: str = "[%(asctime)s] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
    log_level: Literal["debug", "info", "warning", "error"] = "info"
    log_colors: dict[str, str] = {
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    }


class DatabaseConfig(BaseModel):
    """Database config."""

    config: dict[str, Any] = {
        "connections": {
            "default": "sqlite://settings/database/database.db",
        },
        "apps": {
            "models": {
                "models": ["src.utils.database.models"],
                "default_connection": "default",
            },
        },
    }


class Settings(BaseSettings):
    """Settings for the application."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="_",
        case_sensitive=False,
    )

    bot: BotConfig
    color: ColorConfig = ColorConfig()
    emoji: EmojiConfig = EmojiConfig()
    logging: LoggingConfig = LoggingConfig()
    database: DatabaseConfig = DatabaseConfig()


settings = Settings()
