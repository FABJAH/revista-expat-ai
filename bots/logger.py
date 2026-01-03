import logging
import os

_logger = logging.getLogger("revista_expats_ai")
if not _logger.handlers:
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    _logger.setLevel(getattr(logging, level, logging.INFO))
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    _logger.addHandler(handler)

logger = _logger
