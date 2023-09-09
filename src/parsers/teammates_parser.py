from src.parsers.parser import Parser
from src.constants import URL
from src.cache_manager import *
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd


def parse_row_data(soup: BeautifulSoup):
    rows = soup.findAll('tr')[2:]
    rows_data = []
    for i in range(len(rows)):
        row = []
        for td in rows[i].findAll('td'):
            # check if td has a href
            if td.find('a'):
                row.append(td.find('a').get('href').replace('.html', '').split('/')[-1])
            row.append(td.getText())
        rows_data.append(row)
    return [e for e in rows_data if e != []]


def parse_headers(soup: BeautifulSoup):
    headers = [th.getText() for th in soup.findAll('tr', limit=2)[1].findAll('th')]
    headers = headers[1:]
    headers.insert(0, "id")
    prefixes = ["Overall", "Regular Season", "Playoffs"]
    headers_to_change = {"G": 0, "W": 0, "L": 0, "W%": 0}
    for i in range(len(headers)):
        if headers[i] in headers_to_change:
            aux = headers[i]
            headers[i] = prefixes[headers_to_change[headers[i]]] + "-" + headers[i]
            headers_to_change[aux] += 1
    return headers


class TeammatesParser(Parser):
    TEAMMATES_URL = URL + "/friv/teammates_and_opponents.fcgi?pid=%s&type=t"
    CACHE_SUBDIR = "teammates"

    def parse(self, player: str):
        if cache_exists(player, TeammatesParser.CACHE_SUBDIR):
            self._data = get_from_cache(player, TeammatesParser.CACHE_SUBDIR)
            return
        html = urlopen(TeammatesParser.TEAMMATES_URL % player)
        soup = BeautifulSoup(html, features="html.parser")
        headers = parse_headers(soup)
        rows_data = parse_row_data(soup)

        df = pd.DataFrame(rows_data, columns=headers)
        # remove empty columns
        df.drop([""], axis=1, inplace=True)
        self._data = df
        add_to_cache(df, player, TeammatesParser.CACHE_SUBDIR)
