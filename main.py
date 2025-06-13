import os
import logging
import argparse
from datetime import datetime
from src.menu import run_menu

# ---- CLI ARG PARSER ----
parser = argparse.ArgumentParser(description="Run SIPD-RI Helper")
parser.add_argument(
    "--dev", action="store_true", help="Development mode with DEBUG logging"
)
args = parser.parse_args()

# ---- LOGGING SETUP -----
os.makedirs("logs", exist_ok=True)
log_level = logging.DEBUG if args.dev else logging.INFO
log_filename = datetime.now().strftime("logs/%Y-%m-%d.log")
logging.basicConfig(
    level=log_level,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_filename, encoding="utf-8"),
    ],
)

# ---- MAIN EXECUTION ----
if __name__ == "__main__":
    run_menu()
