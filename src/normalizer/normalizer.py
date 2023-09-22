import pandas as pd

from src.workflow.workflow import WorkflowDataKeys
from src.workflow.workflow_object import WorkflowObject


class Normalizer(WorkflowObject):

    def __init__(self, column_map: dict):
        self.column_map = column_map

    def execute(self, data: dict) -> (pd.DataFrame, Exception | None):
        df: pd.DataFrame = data[WorkflowDataKeys.DATASET]
        try:
            df = self.normalize(df)
        except Exception as e:
            return df, e
        return df, None

    def normalize(self, data: pd.DataFrame) -> pd.DataFrame:
        return self.__rename_columns(data)

    def __rename_columns(self, data: pd.DataFrame) -> pd.DataFrame:
        return data.rename(columns=self.column_map)
