import os
import time

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from rich.table import Table
from rich.text import Text
from rich.traceback import Traceback

from src.bot_sipd import SIPDBot
from src.helper_excel import ExcelHelper


def save_cookies():
    with Progress() as progress:
        task = progress.add_task("[green]Saving cookies...", total=100)

        progress.update(task, advance=20, description="Checking cookie existence")
        if SIPDBot.is_cookies_exist():
            os.remove("cookies.json")
            progress.update(task, advance=20, description="Removing old cookies")

        progress.update(task, advance=20, description="Logging in")
        with SIPDBot() as bot:
            bot.login()
        progress.update(task, advance=40, description="Cookie saved!")

    menu_return()


def download_laporan_realisasi(start_month, end_month):
    with SIPDBot() as bot:
        bot.login()
        bot.download_realisasi(start_month, end_month)


def input_jurnal_umum():
    with SIPDBot() as bot:
        pass


# --------------------------------------------------


def menu_clear():
    console = Console()
    console.clear()


def menu_return():
    console = Console()
    console.print("\n> Press Enter to continue...", style="dim")
    input()


def menu_title():
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
    console = Console()
    table = Table(
        show_header=True, show_edge=False, show_lines=False, box=box.HORIZONTALS
    )

    # Coming Soon
    coming_soon = " - :warning:  [italic]On Progress[/italic]"

    # Table Header
    table.add_column("Menu", style="bold red", justify="right")
    table.add_column("Function", style="white")

    # Save cookies
    table.add_row("1", "Save cookies [dim](Please refresh cookies everyday!)[/dim]")
    table.add_row()

    # Akuntansi
    table.add_row("", Text("Akuntansi", style="green bold"))
    table.add_row("a1", "Posting Jurnal")
    table.add_row("a2", "Input Jurnal Umum")
    table.add_row("a3", f"Input Saldo Awal{coming_soon}", style="dim")
    table.add_row()

    # Penatausahaan
    table.add_row("", Text("Penatausahaan", style="green bold"))
    table.add_row("b1", "Download Laporan Realisasi")
    table.add_row("b2", f"Scrape BKU Pajak{coming_soon}", style="dim")
    table.add_row()

    # Misc.
    table.add_row("", Text("Miscellaneous", style="green bold"))
    table.add_row("c1", f"Compile Excel{coming_soon}", style="dim")
    table.add_row("c2", f"Clean Excel{coming_soon}", style="dim")
    table.add_row("c3", f"Convert .xls to .xlsx{coming_soon}", style="dim")
    table.add_row()

    # Exit
    table.add_row("0", "Exit")

    console.print(table)


def run_app():
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

            # 0 - Exit
            elif choice == "0":
                console.print("> :wave: [bold cyan]Good bye...[/bold cyan]")
                time.sleep(1)
                break

            else:
                console.print(
                    "> :warning:  [red]Invalid choice![/red] Please try again."
                )
                menu_return()

    except KeyboardInterrupt:
        console.print("\n> :wave: [bold cyan]Good bye...[/bold cyan]")
        time.sleep(1)

    except Exception:
        console.print(Traceback())
