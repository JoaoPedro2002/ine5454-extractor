from abc import ABC, abstractmethod

import pandas as pd


class WorkflowObject(ABC):
    @abstractmethod
    def execute(self, data: dict) -> (pd.DataFrame, Exception | None):
        raise NotImplementedError("Please Implement this method")
