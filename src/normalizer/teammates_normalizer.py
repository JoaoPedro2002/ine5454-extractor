from src.normalizer.normalizer import Normalizer


class TeammatesNormalizer(Normalizer):
    def __init__(self):
        super().__init__({
            "Teammate": "player",
            "Overall-G": "total_games",
            "Overall-W": "total_wins",
            "Overall-L": "total_losses",
            "Overall-W%": "total_win_percentage",
            "Regular Season-G": "regular_season_games",
            "Regular Season-W": "regular_season_wins",
            "Regular Season-L": "regular_season_losses",
            "Regular Season-W%": "regular_season_win_percentage",
            "Playoffs-G": "playoffs_games",
            "Playoffs-W": "playoffs_wins",
            "Playoffs-L": "playoffs_losses",
            "Playoffs-W%": "playoffs_win_percentage",
        })

    def normalize(self, data):
        return super().normalize(data)
