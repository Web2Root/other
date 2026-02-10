import logging
import sys

import colorlog

from src.utils.config import settings

log_level = getattr(logging, settings.logging.log_level.upper())

formatter = colorlog.ColoredFormatter(
    fmt="%(log_color)s" + settings.logging.log_format,
    datefmt="%Y-%m-%d / %H:%M:%S",
    log_colors=settings.logging.log_colors,
)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
handler.setLevel(log_level)

logging.basicConfig(level=log_level, handlers=[handler])
log = logging.getLogger()
