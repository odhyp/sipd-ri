"""
A helper module for working with Excel files.

Provides functions for reading, manipulating, and potentially other operations on Excel files.
"""

import pandas as pd


class ExcelHelper:
    """
    A helper class for working with Excel files.
    """

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
