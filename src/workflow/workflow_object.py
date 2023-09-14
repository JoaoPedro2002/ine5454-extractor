from enum import Enum
from abc import ABC, abstractmethod

import pandas as pd


class WorkflowExecutionStatus(Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    ABORTED = "ABORTED"


class WorkflowObject(ABC):
    @abstractmethod
    def execute(self, data: dict) -> tuple[WorkflowExecutionStatus, pd.DataFrame | None]:
        raise NotImplementedError("Please Implement this method")
