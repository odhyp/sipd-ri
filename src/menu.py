"""
Interactive command-line interface for the SIPD-RI 2025 Helper.

This menu provides access to various SIPDBot features through a terminal-based interface.
Each option maps to a specific automation task or utility.

Main Menu:
1. Download Lampiran I.1 (Perkada)
   ├─ 1. All OPD
   └─ 2. All UPT
9. Reset session cookies
0. Exit

Usage:
- Navigates using numeric input.
- Submenus are shown when available.
- Invalid inputs will prompt retry.

Structure:
- Each feature is delegated to a handler function for clarity and scalability.
"""

import os
import logging
from src.sipd_bot import SIPDBot

logger = logging.getLogger(__name__)


def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def menu_header():
    """Prints the app header."""
    print("\nSIPD-RI 2025 Helper")
    print("By: Odhy (odhyp.com)\n")


# ---------- 1. Download Lampiran I.1 (Perkada) ----------
def handle_download_perkada():
    while True:
        clear_screen()
        menu_header()

        print("Download Lampiran I.1 (Perkada)")
        print("1. All OPD")
        print("2. All UPT")
        print("0. Back")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            with SIPDBot() as bot:
                bot.login()
                bot.download_lampiran_perkada()
                print("All OPD")
            break

        elif choice == "2":
            with SIPDBot() as bot:
                bot.login()
                bot.download_lampiran_perkada()
                print("All UPT")
            break

        elif choice == "0":
            break

        else:
            input("Invalid choice! Press Enter to continue...")


# ---------- 9. Reset session cookies ----------
def handle_reset_cookies():
    with SIPDBot() as bot:
        bot.reset_cookies()


# ---------- MAIN MENU ----------
def run_menu():
    logger.info("SIPD-RI Helper Menu launched")

    while True:
        clear_screen()
        menu_header()

        print("1. Download Lampiran I.1 (Perkada)")
        print("9. Reset session cookies")
        print("0. Exit")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            handle_download_perkada()

        elif choice == "9":
            handle_reset_cookies()

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            input("Invalid choice! Press Enter to continue...")

    logger.info("SIPD-RI Helper Menu closed")
