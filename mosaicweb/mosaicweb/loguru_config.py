# loguru_config.py

from loguru import logger
import logging
import os
from django.conf import settings

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Configure loguru to log into a file
logger.add(os.path.join(settings.BASE_DIR, "debug.log"), level="DEBUG", format="{time} {level} {message}", rotation="10 MB")

# Optional: Redirect standard logging to loguru
class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())

logging.basicConfig(handlers=[InterceptHandler()], level=logging.DEBUG)
