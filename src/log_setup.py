import os
import logging
from datetime import datetime


def setup_logging(dev_mode: bool):
    os.makedirs("logs", exist_ok=True)
    log_level = logging.DEBUG if dev_mode else logging.INFO
    log_filename = datetime.now().strftime("logs/%Y-%m-%d.log")

    handlers = [logging.FileHandler(log_filename, encoding="utf-8")]

    if dev_mode:
        handlers.append(logging.StreamHandler())  # 👈 Only add console logging in dev

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=handlers,
    )
