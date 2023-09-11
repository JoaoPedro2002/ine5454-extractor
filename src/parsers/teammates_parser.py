from src.parsers.parser import Parser
from src.constants import URL
from bs4 import BeautifulSoup


class TeammatesParser(Parser):
    TEAMMATES_URL = URL + "/friv/teammates_and_opponents.fcgi?pid=%s&type=t"
    CACHE_SUBDIR = "teammates"

    def parse_row_data(self, soup: BeautifulSoup):
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

    def parse_headers(self, soup: BeautifulSoup):
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

    def get_url(self) -> str:
        return TeammatesParser.TEAMMATES_URL

    def get_cache_subdir(self) -> str:
        return TeammatesParser.CACHE_SUBDIR
