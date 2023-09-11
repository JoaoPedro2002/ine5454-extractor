from src.parsers.parser import Parser
from src.constants import URL
from bs4 import BeautifulSoup


class PlayerIdParser(Parser):
    PLAYER_ID_URL = URL + "/players/%s/"
    CACHE_SUBDIR = "players_ids"

    def parse_row_data(self, soup: BeautifulSoup):
        rows = soup.findAll('tr')[1:]
        rows_data = []
        for i in range(len(rows)):
            row = [td.getText() for td in rows[i].findAll('td')]
            rows_data.append(row)
            th = rows[i].find('th')
            if not th:
                continue
            row.insert(0, th.getText())
            if th.find('a'):
                row.insert(0, th.find('a').get('href').replace('.html', '').split('/')[-1])
        return [e for e in rows_data if e != []]

    def parse_headers(self, soup: BeautifulSoup):
        headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
        headers.insert(0, "id")
        return headers

    def get_url(self) -> str:
        return PlayerIdParser.PLAYER_ID_URL

    def get_cache_subdir(self) -> str:
        return PlayerIdParser.CACHE_SUBDIR





