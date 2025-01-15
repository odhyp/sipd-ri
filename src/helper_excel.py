"""
A helper module for working with Excel files.

Provides functions for reading, manipulating, and potentially other operations on Excel files.
"""

import pandas as pd
import os

from win32com.client import Dispatch, DispatchEx


class ExcelHelper:
    """
    A helper class for working with Excel files.
    """

    @staticmethod
    def resave_excel(file_path: str):
        """
        Opens an Excel file using Win32Com, resaves it at the same location and add `compressed`
        in its file name.

        Args:
            file_path (str): Path to the existing Excel file.
        """
        try:
            file_path = os.path.abspath(file_path)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"The file '{file_path}' does not exist.")

            # Create the new file name with "compressed" added before the extension
            base_name, ext = os.path.splitext(file_path)
            compressed_file_path = f"{base_name}_compressed{ext}"

            # Initialize Excel application (using DispatchEx for isolation)
            excel = DispatchEx("Excel.Application")
            workbook = excel.Workbooks.Open(file_path)
            workbook.SaveAs(compressed_file_path, FileFormat=51)
            workbook.Close()
            excel.Quit()

            return compressed_file_path

        # Ensure Excel quits in case of error
        except Exception as e:
            try:
                excel.Quit()
            except RuntimeError:
                return f"Failed to resave Excel file: {e}"

    @staticmethod
    def read_jurnal_umum(file_path: str) -> list:
        """
        Read an excel file of Jurnal Umum and store the values in list.

        Args:
            file_path (str): The path to Excel file for Jurnal Umum.

        Returns:
            list: The list of Jurnal Umum.
        """
        df = pd.read_excel(file_path)
        jurnal_umum = df.values.tolist()
        return jurnal_umum
