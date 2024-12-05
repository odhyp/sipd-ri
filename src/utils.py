import os
from pathlib import Path
from datetime import datetime


def get_month_name(index):
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
    return month_list[index - 1]


def get_current_time() -> str:
    return datetime.now().strftime("%H:%M:%S")


def get_current_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")


class PathHelper:

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
