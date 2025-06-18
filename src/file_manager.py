import tkinter as tk
from tkinter import filedialog


class FileManager:
    @staticmethod
    def select_file():
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename(
            title="Pilih file", filetypes=[("Excel file", "{*.xlsx}")]
        )

        if file_path:
            print(f"File dipilih: {file_path}")
            return file_path
        else:
            return None
