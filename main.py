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

import logging
import argparse
from src.menu import run_menu
from src.log_setup import setup_logging


# ---- CLI ARG PARSER ----
# TODO: replace with Rich or Typer
parser = argparse.ArgumentParser(description="Run SIPD-RI Helper")
parser.add_argument(
    "--dev", action="store_true", help="Development mode with DEBUG logging"
)
args = parser.parse_args()


# ---- LOGGING SETUP -----
setup_logging(args.dev)

logger = logging.getLogger(__name__)
if args.dev:
    logger.debug("Running in development mode with DEBUG logging enabled")


# ---- MAIN EXECUTION ----
if __name__ == "__main__":
    run_menu()
