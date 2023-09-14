import os
from pandas import DataFrame, read_csv

from src.constants import CACHE_PATH


class CacheManager:
    PLAYER_ID_CACHE_SUBDIR = "players_ids"
    TEAMMATES_CACHE_SUBDIR = "teammates"

    def __init__(self, subdir: str):
        self.__subdir = subdir

    def cache_exists(self, identifier: str) -> bool:
        return os.path.exists(os.path.join(CACHE_PATH, self.__subdir, identifier + '.csv'))

    def get_from_cache(self, identifier: str) -> DataFrame:
        return read_csv(os.path.join(CACHE_PATH, self.__subdir, identifier + '.csv'))

    def add_to_cache(self, data: DataFrame, identifier: str):
        if not os.path.exists(os.path.join(CACHE_PATH, self.__subdir)):
            os.makedirs(os.path.join(CACHE_PATH, self.__subdir))
        data.to_csv(os.path.join(CACHE_PATH, self.__subdir, identifier + '.csv'), index=False)
