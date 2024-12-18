import pandas as pd


class ExcelHelper:
    """ """

    @staticmethod
    def read_jurnal_umum(file_path: str):
        df = pd.read_excel(file_path)
        jurnal_umum = df.values.tolist()
        return jurnal_umum
