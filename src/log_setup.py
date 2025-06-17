"""
Sets up logging for SIPDBot with file and optional console output.

Logs are saved daily in the `logs/` folder, and in dev mode,
messages are also printed to the console.
"""

import os
import logging
from datetime import datetime


def setup_logging(dev_mode: bool):
    """
    Initialize logging with file and optional console output.

    Args:
        dev_mode (bool): Enables DEBUG level and console logging if True.
    """
    os.makedirs("logs", exist_ok=True)
    log_level = logging.DEBUG if dev_mode else logging.INFO
    log_filename = datetime.now().strftime("logs/%Y-%m-%d.log")

    handlers = [logging.FileHandler(log_filename, encoding="utf-8")]

    if dev_mode:
        handlers.append(logging.StreamHandler())

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=handlers,
    )
