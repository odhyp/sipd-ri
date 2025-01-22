"""
A helper module for generating menu screen, user interactions, and compiling functions.
"""

import os
import time

from rich import box
from rich.console import Console
from rich.progress import Progress
from rich.table import Table
from rich.text import Text
from rich.traceback import Traceback

from src.bot_sipd import SIPDBot
from src.helper_excel import ExcelHelper
from src.utils import select_excel_file, select_excel_files, get_current_date


def save_cookies():
    with Progress() as progress:
        task = progress.add_task("[green]Saving cookies...", total=100)

        progress.update(task, advance=20, description="Checking cookie existence")
        if SIPDBot.is_cookies_exist():
            os.remove("cookies.json")
            progress.update(task, advance=20, description="Removing old cookies")
        else:
            progress.update(task, advance=20, description="Cookie not found")

        progress.update(task, advance=20, description="Logging in")
        with SIPDBot() as bot:
            bot.login()
        progress.update(task, advance=40, description="Cookie saved!")


# ---------- a2 - beta success
def input_jurnal_umum(file_path):
    jurnal_umum = ExcelHelper.read_jurnal_umum(file_path)

    with SIPDBot() as bot:
        bot.login()
        bot.input_jurnal_umum(jurnal_umum)


# ---------- a3 - good as intended
def download_neraca():
    today = get_current_date()
    output_dir = f"LK - Neraca {today}"

    skpd_list = []
    with open("data/SKPD-2024.txt", mode="r", encoding="utf-8") as file:
        skpd_list = [line.strip() for line in file]

    with SIPDBot() as bot:
        bot.login()
        bot.download_neraca(output_dir, skpd_list)


# ---------- a4 - good as intended
def download_lra():
    today = get_current_date()
    output_dir = f"LK - LRA {today}"

    skpd_list = []
    with open("data/SKPD-2024.txt", mode="r", encoding="utf-8") as file:
        skpd_list = [line.strip() for line in file]

    with SIPDBot() as bot:
        bot.login()
        bot.download_lra(output_dir, skpd_list)


# ---------- a5 - good as intended
def download_lo():
    today = get_current_date()
    output_dir = f"LK - LO {today}"

    skpd_list = []
    with open("data/SKPD-2024.txt", mode="r", encoding="utf-8") as file:
        skpd_list = [line.strip() for line in file]

    with SIPDBot() as bot:
        bot.login()
        bot.download_lo(output_dir, skpd_list)


# ---------- a6 - good as intended
def download_lpe():
    today = get_current_date()
    output_dir = f"LK - LPE {today}"

    skpd_list = []
    with open("data/SKPD-2024.txt", mode="r", encoding="utf-8") as file:
        skpd_list = [line.strip() for line in file]

    with SIPDBot() as bot:
        bot.login()
        bot.download_lpe(output_dir, skpd_list)


# ---------- a7 - good as intended
def download_buku_jurnal():
    today = get_current_date()
    output_dir = f"Buku Jurnal {today}"

    # FIXME: Update using Tkinter file select
    skpd_path = "data/DIKPORA-dan-anak.txt"

    skpd_list = []
    with open(skpd_path, mode="r", encoding="utf-8") as file:
        skpd_list = [line.strip() for line in file]

    with SIPDBot() as bot:
        bot.login()
        bot.download_buku_jurnal(output_dir, skpd_list)


# ---------- b1
def download_laporan_realisasi(start_month, end_month):
    today = get_current_date()
    output_dir = f"Laporan Realisasi {today}"

    with SIPDBot() as bot:
        bot.login()
        bot.download_realisasi(output_dir, start_month, end_month)


# ---------- Displayed Menu functions -----------------------------------------
def menu_clear():
    """
    Clear the console screen.
    """
    console = Console()
    console.clear()


def menu_return():
    """
    Print out user input to halt current process.
    """
    console = Console()
    console.print("\n> Press Enter to continue...", style="dim")
    input()


def menu_title():
    """
    Prints out the menu title.
    """
    console = Console()

    # Title and version
    console.print(
        Text("SIPD-RI Helper", style="bold cyan"),
        Text("ver 0.1.0", style="bold white"),
    )

    # Author
    console.print(
        Text("By Odhy Pradhana -", style="italic dim"),
        Text("odhyp.com", style="underline dim"),
        "\n\n",
    )


def menu_table():
    """
    Prints out the menu table.
    """
    console = Console()
    table = Table(
        show_header=True, show_edge=False, show_lines=False, box=box.HORIZONTALS
    )

    # Coming Soon
    coming_soon = " - :warning:  [italic]On Progress[/italic]"

    # Table Header
    table.add_column("Menu", style="bold red", justify="right")
    table.add_column("Function", style="white")

    # Common Menu
    table.add_row("0", "Exit")
    table.add_row("1", "Save cookies [dim](Please refresh cookies everyday!)[/dim]")
    table.add_row()

    # Akuntansi
    table.add_row("", Text("Akuntansi", style="green bold"))
    table.add_row("a1", f"Posting Jurnal{coming_soon}", style="dim")
    table.add_row("a2", "Input Jurnal Umum")
    table.add_row("a3", "Download LK - Neraca")
    table.add_row("a4", "Download LK - LRA")
    table.add_row("a5", "Download LK - LO")
    table.add_row("a6", "Download LK - LPE")
    table.add_row("a7", "Download Buku Jurnal")
    table.add_row()

    # Penatausahaan
    table.add_row("", Text("Penatausahaan", style="green bold"))
    table.add_row("b1", "Download Laporan Realisasi")
    table.add_row("b2", f"Scrape BKU Pajak{coming_soon}", style="dim")
    table.add_row()

    # Misc.
    table.add_row("", Text("Miscellaneous", style="green bold"))
    table.add_row("c1", "Resave Excel - Test")
    table.add_row("c2", f"Clean Excel{coming_soon}", style="dim")
    table.add_row("c3", f"Convert .xls to .xlsx{coming_soon}", style="dim")
    table.add_row()

    console.print(table)


def run_app():
    """
    Run the command-line application.
    """
    console = Console()

    try:
        while True:
            menu_clear()
            menu_title()
            menu_table()

            choice = input("\n> ")

            # 1 - Save Cookies
            if choice == "1":
                menu_clear()
                menu_title()
                save_cookies()

            # a1 - Posting Jurnal
            elif choice == "a1":
                menu_clear()
                menu_title()

                console.print("Test Posting Jurnal", style="blue")
                try:
                    posting_jurnal()
                except Exception:
                    console.print(Traceback())
                else:
                    pass
                finally:
                    menu_return()

            # a2 - Input Jurnal Umum
            elif choice == "a2":
                menu_clear()
                menu_title()

                console.print("Input Jurnal Umum - Test Function", style="blue")
                try:
                    file_path = "jurnal_umum.xlsx"
                    input_jurnal_umum(file_path)
                except Exception:
                    console.print(Traceback())
                else:
                    pass
                finally:
                    menu_return()

            # a3 - Download LK - Neraca
            elif choice == "a3":
                menu_clear()
                menu_title()

                console.print("Download LK Neraca - Test Function", style="blue")
                try:
                    download_neraca()
                except Exception:
                    console.print(Traceback())
                else:
                    pass
                finally:
                    menu_return()

            # a4 - Download LK - LRA
            elif choice == "a4":
                menu_clear()
                menu_title()

                console.print("Download LK LRA - Test Function", style="blue")
                try:
                    download_lra()
                except Exception:
                    console.print(Traceback())
                else:
                    pass
                finally:
                    menu_return()

            # a5 - Download LK - LO
            elif choice == "a5":
                menu_clear()
                menu_title()

                console.print("Download LK LO - Test Function", style="blue")
                try:
                    download_lo()
                except Exception:
                    console.print(Traceback())
                else:
                    pass
                finally:
                    menu_return()

            # a6 - Download LK - LPE
            elif choice == "a6":
                menu_clear()
                menu_title()

                console.print("Download LK LPE - Test Function", style="blue")
                try:
                    download_lpe()
                except Exception:
                    console.print(Traceback())
                else:
                    pass
                finally:
                    menu_return()

            # a7 - Download Buku Jurnal
            elif choice == "a7":
                menu_clear()
                menu_title()

                console.print("Download Buku Jurnal - Test Function", style="blue")
                try:
                    download_buku_jurnal()
                except Exception:
                    console.print(Traceback())
                else:
                    pass
                finally:
                    menu_return()

            # b1 - Download Laporan Realisasi
            elif choice == "b1":
                menu_clear()
                menu_title()

                console.print("Download Laporan Realisasi", style="blue")
                try:
                    start_month = int(input("Enter start month: "))
                    end_month = int(input("Enter end month: "))
                    download_laporan_realisasi(start_month, end_month)
                except Exception:
                    console.print(Traceback())
                else:
                    pass
                finally:
                    menu_return()

            # 0 - Exit
            elif choice == "0":
                console.print("> :wave: [bold cyan]Good bye...[/bold cyan]")
                time.sleep(1)
                break

            else:
                console.print(
                    "> :warning:  [red]Invalid choice![/red] Please try again."
                )
                # menu_return()

    except KeyboardInterrupt:
        console.print("\n> :wave: [bold cyan]Good bye...[/bold cyan]")
        time.sleep(1)

    except Exception:
        console.print(Traceback())
