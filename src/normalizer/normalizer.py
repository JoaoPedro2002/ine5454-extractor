import pandas as pd

from src.workflow.workflow import WorkflowDataKeys
from src.workflow.workflow_object import WorkflowObject, WorkflowExecutionStatus


class Normalizer(WorkflowObject):

    def __init__(self, column_map: dict):
        self.column_map = column_map

    def execute(self, data: dict) -> tuple[WorkflowExecutionStatus, pd.DataFrame | None]:
        try:
            df = self.normalize(data[WorkflowDataKeys.DATASET])
        except Exception:
            return WorkflowExecutionStatus.FAILED, None
        return WorkflowExecutionStatus.SUCCESS, df

    def normalize(self, data: pd.DataFrame) -> pd.DataFrame:
        return self.__rename_columns(data)

    def __rename_columns(self, data: pd.DataFrame) -> pd.DataFrame:
        return data.rename(columns=self.column_map)
