"""
Utility module for date, time, and file path operations.
Provides common operations with getters.
"""

import os
from pathlib import Path
from datetime import datetime

import tkinter as tk
from tkinter import filedialog


def select_excel_file() -> str:
    """
    Opens a file selection dialog and returns the chosen Excel filepath.

    Returns:
        str: The absolute path to the selected Excel file,
             or an empty string if the user cancels.
    """
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    root.destroy()
    return file_path


def select_excel_files() -> tuple:
    """
    Opens a file selection dialog and returns a tuple of chosen Excel filepaths.

    Returns:
        tuple: A tuple containing the absolute paths to the selected Excel files,
               or an empty tuple if the user cancels.
    """
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(filetypes=[("Excel files", "*.xlsx")])
    root.destroy()
    return file_paths


def get_month_name(index) -> str:
    """
    Get the name of the month corresponding to the given index.

    Args:
        index (int): The index of the month (1 for January, 12 for December).

    Returns:
        str: The name of the month in Indonesian.
        None: If the index is outside the range 1-12.
    """
    month_list = [
        "Januari",
        "Februari",
        "Maret",
        "April",
        "Mei",
        "Juni",
        "Juli",
        "Agustus",
        "September",
        "Oktober",
        "November",
        "Desember",
    ]
    try:
        return month_list[index - 1]
    except IndexError:
        return None


def get_current_time() -> str:
    """
    Get the current time in HH:MM:SS format.

    Returns:
        str: The current time as a string formatted as `HH.MM`.
    """
    return datetime.now().strftime("%H.%M")


def get_current_date() -> str:
    """
    Get the current date in YYYY-MM-DD format.

    Returns:
        str: The current date as a string formatted as `YYYY-MM-DD`.
    """
    return datetime.now().strftime("%Y-%m-%d")


class PathHelper:
    """
    A utility class for managing file paths.
    """

    @staticmethod
    def get_current_dir() -> str:
        return Path(os.getcwd())

    @staticmethod
    def get_download_path() -> str:
        pass

    @staticmethod
    def get_root_path() -> str:
        root_path = Path(os.getcwd())
        return str(root_path)

    @staticmethod
    def get_output_path(output_dir: str, file_name: str) -> str:
        output_path = Path("output", output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        output_path = Path(output_path, file_name)
        return str(output_path)
