import pandas as pd
from .normalizer import Normalizer

FEET_TO_CM = 30.48
INCHES_TO_CM = 2.54


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

    def normalize(self, data: pd.DataFrame) -> pd.DataFrame:
        def height_to_cm(x):
            feet, inches = x.split('-')
            return round(int(feet) * FEET_TO_CM + int(inches) * INCHES_TO_CM)

        data = super().normalize(data)
        data['birth_date'] = pd.to_datetime(data['birth_date'], format='%B %d, %Y')
        data['player'] = data['player'].str.replace('*', '')
        # convert height to cm
        data['height'] = data['height'].apply(height_to_cm)
        return data
