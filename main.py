"""
Main entry point for the SIPD-RI Helper CLI.

This script sets up command-line argument parsing and logging configuration,
then launches the interactive menu interface for performing automated actions
on the SIPD-RI web application.

Usage:
    python main.py [--dev]

Arguments:
    --dev : Run the tool in development mode with DEBUG-level logging.

Logs:
    Log files are stored in the `logs/` directory, named by date (e.g. 2025-06-10.log).
"""

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
LOG_LEVEL = logging.DEBUG if args.dev else logging.INFO
log_filename = datetime.now().strftime("logs/%Y-%m-%d.log")
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_filename, encoding="utf-8"),
    ],
)

logger = logging.getLogger(__name__)
if args.dev:
    logger.debug("Running in development mode with DEBUG logging enabled")


# ---- MAIN EXECUTION ----
if __name__ == "__main__":
    run_menu()
