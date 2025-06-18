"""
Interactive command-line interface for the SIPD-RI 2025 Helper.

This menu provides access to various SIPDBot features through a terminal-based interface.
Each option maps to a specific automation task or utility.

Main Menu:
1. Jurnal Umum
   ├─ 1. Input Jurnal Umum
   └─ 0. Kembali
2. Download Lampiran I.1 (Perkada)
   ├─ 1. Semua OPD
   ├─ 2. Semua UPT
   └─ 0. Kembali
9. Reset session cookies
0. Keluar

Usage:
- Navigates using numeric input.
- Submenus are shown when available.
- Invalid inputs will prompt retry.

Structure:
- Each feature is delegated to a handler function for clarity and scalability.
"""

import os
import logging
import pandas as pd
from src.sipd_bot import SIPDBot
from src.file_manager import FileManager

logger = logging.getLogger(__name__)


def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def menu_header():
    """Prints the app header."""
    print("\nSIPD-RI 2025 Helper")
    print("By: Odhy (odhyp.com)\n")


# ---------- 1. Jurnal Umum ----------
def handle_jurnal_umum():
    while True:
        clear_screen()
        menu_header()

        print("---------- Jurnal Umum ----------")
        print("1. Input Jurnal Umum")
        print("0. Kembali")

        choice = input("\nPilih opsi: ").strip()

        if choice == "1":
            file_path = FileManager.select_file()
            if not file_path:
                continue

            df = pd.read_excel(file_path, dtype=str)
            jurnal_umum = df.values.tolist()

            with SIPDBot() as bot:
                bot.login()
                bot.input_jurnal_umum(jurnal_umum)
            break

        elif choice == "0":
            break

        else:
            input("Pilihan tidak valid! Tekan Enter untuk melanjutkan...")


# ---------- 2. Download Lampiran I.1 (Perkada) ----------
# TODO: update perkada (Sub-menu) to Lampiran (Menu) instead
def handle_download_perkada():
    while True:
        clear_screen()
        menu_header()

        print("---------- Download Lampiran I.1 (Perkada) ----------")
        print("1. Semua OPD")
        print("2. Semua UPT")
        print("0. Kembali")

        choice = input("\nPilih opsi: ").strip()

        if choice == "1":
            output_dir = "Lampiran_Perkada_OPD"
            skpd_list = []
            with open("data/SKPD-2024.txt", mode="r", encoding="utf-8") as f:
                skpd_list = [line.strip() for line in f]

            with SIPDBot() as bot:
                bot.login()
                bot.download_lampiran_perkada(output_dir, skpd_list)
            break

        elif choice == "2":
            output_dir = "Lampiran_Perkada_UPT"
            skpd_kpa_list = []
            with open("data/SKPD-KPA-2024.txt", mode="r", encoding="utf-8") as f:
                skpd_kpa_list = [line.strip() for line in f]

            with SIPDBot() as bot:
                bot.login()
                bot.download_lampiran_perkada(output_dir, skpd_kpa_list)
            break

        elif choice == "0":
            break

        else:
            input("Pilihan tidak valid! Tekan Enter untuk melanjutkan...")


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

        print("---------- Akuntansi ----------")
        print("1. Jurnal Umum")
        print("2. Download Lampiran I.1 (Perkada)")

        print("\n---------- Lain-lain ----------")
        print("9. Reset cookies")
        print("0. Keluar")

        choice = input("\nPilih opsi: ").strip()

        if choice == "1":
            handle_jurnal_umum()

        elif choice == "2":
            handle_download_perkada()

        elif choice == "9":
            handle_reset_cookies()

        elif choice == "0":
            print("Selamat tinggal!")
            break

        else:
            input("Pilihan tidak valid! Tekan Enter untuk melanjutkan...")

    logger.info("SIPD-RI Helper Menu closed")
