import pandas as pd
from dataclasses import dataclass


@dataclass
class WorkflowOutput:
    df: pd.DataFrame
    exception: Exception = None
    online: bool = True

    @staticmethod
    def from_cache(df: pd.DataFrame):
        return WorkflowOutput(df, online=False)

    @staticmethod
    def success(df: pd.DataFrame):
        return WorkflowOutput(df)

    @staticmethod
    def failed(df: pd.DataFrame, exception: Exception):
        return WorkflowOutput(df, exception=exception)
