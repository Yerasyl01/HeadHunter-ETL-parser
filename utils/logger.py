from loguru import logger
from config import settings

logger.remove()
logger.add(
    sink=lambda message: print(message, end=""),
    level=settings.log_level,
)

__all__ = ["logger"]
