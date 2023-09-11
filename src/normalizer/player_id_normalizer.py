import pandas as pd
from .normalizer import Normalizer


class PlayerIdNormalizer(Normalizer):

    def __init__(self):
        super().__init__({
            "Player": "player",
            "From": "from",
            "To": "to",
            "Pos": "position",
            "Ht": "height",
            "Wt": "weight",
            "Birth Date": "birth_date",
            "Colleges": "colleges"
        })

    def normalize(self, data: pd.DataFrame):
        super().normalize(data)
        data['birth_date'] = pd.to_datetime(data['Birth Date'], format='%Y-%m-%d')
