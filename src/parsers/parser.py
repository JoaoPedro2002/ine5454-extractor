from src.cache_manager import *
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd


class Parser:
    def __init__(self):
        self._data = None

    def parse(self, identifier: str):
        if cache_exists(identifier, self.get_cache_subdir()):
            self._data = get_from_cache(identifier, self.get_cache_subdir())
            print(f"Found {self.get_cache_subdir()}/{identifier}.csv in cache")
            return
        html = urlopen(self.get_url() % identifier)
        soup = BeautifulSoup(html, features="html.parser")
        headers = self.parse_headers(soup)
        rows_data = self.parse_row_data(soup)

        df = pd.DataFrame(rows_data, columns=headers)
        # remove empty columns
        try:
            df.drop([""], axis=1, inplace=True)
        except KeyError:
            pass
        self._data = df
        add_to_cache(df, identifier, self.get_cache_subdir())

    def print(self):
        if self._data is None:
            raise Exception("No data to print")
        print(self._data)

    def save_csv(self, path: str):
        if self._data is None:
            raise Exception("No data to save")
        self._data.to_csv(path, index=False)

    def to_json(self) -> map:
        if self._data is None:
            raise Exception("No data to save")
        return self._data.to_json(orient="records")

    def get_data(self) -> pd.DataFrame:
        if self._data is None:
            raise Exception("No data to return")
        return self._data

    def parse_row_data(self, soup: BeautifulSoup) -> list[list[str]]:
        raise NotImplementedError("This method must be implemented by subclasses")

    def parse_headers(self, soup: BeautifulSoup) -> list[str]:
        raise NotImplementedError("This method must be implemented by subclasses")

    def get_url(self) -> str:
        raise NotImplementedError("This method must be implemented by subclasses")

    def get_cache_subdir(self) -> str:
        raise NotImplementedError("This method must be implemented by subclasses")