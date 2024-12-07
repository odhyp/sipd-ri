import os
import time

from src.bot_sipd import SIPDBot
from src.helper_excel import ExcelHelper
from src.helper_cookies import CookieHelper


def download_laporan_realisasi(start_month, end_month):
    bot = SIPDBot()

    if CookieHelper.is_cookies_exist():
        bot.login_with_cookies()
    else:
        bot.login_manual()

    bot.download_realisasi(start_month, end_month)
    bot.close_browser()


def menu_return():
    return input("\nPress Enter to return to the menu...")


def menu_clear():
    os.system("cls" if os.name == "nt" else "clear")


def main_menu():
    try:
        while True:
            menu_clear()

            # MAIN MENU
            print("----- SIPD-RI Helper by Odhy -----\n")
            print("1. Login/save cookies")
            print("2. Download Laporan Realisasi")
            print("0. Exit")

            choice = input("Enter your choice: ").strip()

            # EXIT CODE
            if choice == "0":
                print("\nGoodbye!")
                time.sleep(1)
                break

            # LOGIN/SAVE COOKIES
            if choice == "1":
                menu_clear()
                print("----- Save Cookies -----\n")
                CookieHelper.save_cookies()

            # DOWNLOAD LAPORAN REALIISASI
            elif choice == "2":
                menu_clear()
                print("----- Download Laporan Realisasi -----\n")

                try:
                    start_month = int(input("Start month: "))
                    end_month = int(input("End month: "))
                except Exception as e:
                    print(e)
                else:
                    download_laporan_realisasi(start_month, end_month)
                    menu_return()

            elif choice == "3":
                menu_clear()

                menu_return()

            else:
                print("\nInvalid choice. Please try again.")
                input("Press Enter to return to the menu...")

    except KeyboardInterrupt:
        print("\n\nAction canceled")
        menu_return()
        main_menu()

    except Exception as e:
        print(e)
        menu_return()
        main_menu()
