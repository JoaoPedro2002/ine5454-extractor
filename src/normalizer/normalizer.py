import pandas as pd


class Normalizer:

    def __init__(self, column_map: dict):
        self.column_map = column_map

    def normalize(self, data: pd.DataFrame):
        self.__rename_columns(data)

    def __rename_columns(self, data: pd.DataFrame):
        data.rename(columns=self.column_map)
