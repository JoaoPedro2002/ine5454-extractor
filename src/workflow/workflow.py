from enum import Enum

import pandas as pd

from src.cache_manager import CacheManager
from src.workflow.workflow_object import WorkflowObject, WorkflowExecutionStatus


# enum with keys for workflow data
class WorkflowDataKeys(Enum):
    IDENTIFIER = "identifier"
    DATASET = "dataset"
    SOUP = "soup"


class Workflow:
    """
    Workflow class that executes a list of workflow objects
    The workflow objects are executed in the order they are passed to the constructor, and it's up to the user to
    ensure that the order is correct
    The goal of this class is to provide a simple way to execute the steps of a workflow to process data with the final
    result being a pandas dataframe
    """
    def __init__(self, workflow_name: str,
                 workflow_description: str,
                 workflow_objects: list[type[WorkflowObject]],
                 cache_manager: CacheManager = None):
        self.__workflows = workflow_objects
        self.__workflow_name = workflow_name
        self.__workflow_description = workflow_description
        self.__cache_manager = cache_manager

    def execute(self, data: dict[WorkflowDataKeys, any]) -> pd.DataFrame:
        if self.__cache_manager is not None and self.__cache_manager.cache_exists(data[WorkflowDataKeys.IDENTIFIER]):
            print(f"Found cached data for {data[WorkflowDataKeys.IDENTIFIER]}")
            return self.__cache_manager.get_from_cache(data[WorkflowDataKeys.IDENTIFIER])

        df = None
        for workflow_object in self.__workflows:
            workflow_instance = workflow_object()
            status, df = workflow_instance.execute(data)
            if status != WorkflowExecutionStatus.SUCCESS:
                print(f"Workflow {self.__workflow_name} failed with status {status}")
                return df
            data[WorkflowDataKeys.DATASET] = df

        if self.__cache_manager is not None:
            self.__cache_manager.add_to_cache(df, data[WorkflowDataKeys.IDENTIFIER])

        return df
