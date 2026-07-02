import logging
from datetime import datetime
from pathlib import Path
from config import settings

# Create logs directory if it doesn't exist
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

log_file = log_dir / f"hh_etl_{datetime.now():%Y-%m-%d_%H-%M-%S}.log"

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

root_logger = logging.getLogger()
root_logger.setLevel(settings.log_level.upper())

# Avoid duplicate handlers if this module is imported multiple times
root_logger.handlers.clear()

# Console
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
root_logger.addHandler(console_handler)

# File
file_handler = logging.FileHandler(
    log_file,
    encoding="utf-8",
)
file_handler.setFormatter(formatter)
root_logger.addHandler(file_handler)

logging.getLogger("httpx").setLevel(logging.WARNING)
