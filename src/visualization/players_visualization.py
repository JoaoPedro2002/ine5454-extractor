import os

import pandas as pd

from src.cache_manager import CacheManager
from src.constants import CACHE_PATH
import matplotlib.pyplot as plt


def players_by_position(players: pd.DataFrame) -> pd.DataFrame:
    players_by_position = players.groupby('position').size().reset_index(name='counts')
    players_by_position = players_by_position.sort_values(by=['counts'], ascending=False)
    #plot
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(111)
    ax.bar(players_by_position['position'], players_by_position['counts'])


def players_by_height(players: pd.DataFrame) -> pd.DataFrame:
    players_by_height = players.groupby('height').size().reset_index(name='counts')
    players_by_height = players_by_height.sort_values(by=['counts'], ascending=False)
    #plot
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(111)
    ax.bar(players_by_height['height'], players_by_height['counts'])


def players_by_time(start_year: int, end_year: int, players: pd.DataFrame) -> pd.DataFrame:
    n_players_year = []
    for year in range(start_year, end_year):
        n_players_year.append(len((players[(players['from'] <= year) & (players['to'] >= year)])))
    #plot
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(111)
    ax.plot([str(i) for i in range(start_year, end_year)], n_players_year)

def get_players():
    path = os.path.join(CACHE_PATH, CacheManager.PLAYER_ID_CACHE_SUBDIR)
    players_dfs = []
    for filename in os.listdir(path):
        if not filename.endswith(".csv"):
            continue
        df = pd.read_csv(os.path.join(path, filename))
        players_dfs.append(df)
    return pd.concat(players_dfs)


if __name__ == '__main__':
    players = get_players()
    players_by_position(players)
    players_by_height(players)
    players_by_time(2000, 2020, players)
    plt.show()
