import os
import time

from src.bot_sipd import SIPDBot
from src.helper_excel import ExcelHelper


def save_cookies():
    username = os.getenv("SIPD_USERNAME")
    password = os.getenv("SIPD_PASSWORD")

    bot = SIPDBot()
    bot.save_cookies(username, password)


def download_laporan_realisasi(start_month, end_month):
    bot = SIPDBot()
    bot.download_realisasi(start_month, end_month)
    bot.close_browser()


def menu_return():
    return input("\nPress Enter to return to the menu...")


def menu_clear():
    os.system("cls" if os.name == "nt" else "clear")


def main_menu():
    while True:
        menu_clear()

        # Main menu
        print("Main Menu")
        print("1. Login/save cookies")
        print("2. Download Laporan Realisasi")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        # EXIT CODE
        if choice == "0":
            print("Exiting the menu. Goodbye!")
            break

        # LOGIN/SAVE COOKIES
        elif choice == "1":
            print("----- Save Cookies -----")
            save_cookies()

        # DOWNLOAD LAPORAN REALIISASI
        elif choice == "2":
            print("----- Download Laporan Realisasi -----")

            start_month = int(input("Start month: "))
            end_month = int(input("End month: "))

            download_laporan_realisasi(start_month, end_month)
            menu_return()

        else:
            print("\nInvalid choice. Please try again.")
            input("Press Enter to return to the menu...")
