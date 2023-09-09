import os
from pandas import DataFrame

CACHE_PATH = os.path.join(os.path.dirname(__file__), '.cache')


def cache_exists(identifier: str, subdir: str) -> bool:
    return os.path.exists(os.path.join(CACHE_PATH, subdir, identifier + '.csv'))


def get_from_cache(identifier: str, subdir: str) -> DataFrame:
    with open(os.path.join(CACHE_PATH, subdir, identifier + '.csv'), 'r') as f:
        return DataFrame(f)


def add_to_cache(data: DataFrame, identifier: str, subdir: str):
    if not os.path.exists(os.path.join(CACHE_PATH, subdir)):
        os.makedirs(os.path.join(CACHE_PATH, subdir))
    with open(os.path.join(CACHE_PATH, subdir, identifier + '.csv'), 'w') as f:
        data.to_csv(f, index=False)

