from enum import Enum
from typing import Any

import pandas as pd

from src.cache_manager import CacheManager
from src.logger import LOGGER
from src.workflow.workflow_object import WorkflowObject
from src.workflow.workflow_output import WorkflowOutput


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
                 workflow_objects: [type[WorkflowObject]],
                 cache_manager: CacheManager = None,
                 parse_already_in_cache: bool = True):
        """
        :param workflow_name: name of the workflow
        :param workflow_description:  description of the workflow
        :param workflow_objects: list of workflow objects to execute
        :param cache_manager: cache manager to use for caching the results of the workflow
        :param parse_already_in_cache: if True, the workflow will parse the data even if it's already in the cache
        """
        self.__workflows = workflow_objects
        self.__workflow_name = workflow_name
        self.__workflow_description = workflow_description
        self.__cache_manager = cache_manager
        self.__parse_already_in_cache = parse_already_in_cache

    def execute(self, data: dict[WorkflowDataKeys, Any]) -> WorkflowOutput:
        if self.__cache_manager is not None and self.__cache_manager.cache_exists(data[WorkflowDataKeys.IDENTIFIER]):
            LOGGER.info(f"Found cached data for {data[WorkflowDataKeys.IDENTIFIER]}")
            df = self.__cache_manager.get_from_cache(data[WorkflowDataKeys.IDENTIFIER]) \
                if self.__parse_already_in_cache else None
            return WorkflowOutput.from_cache(df)

        df: pd.DataFrame | None = None
        for workflow_object in self.__workflows:
            workflow_instance = workflow_object()
            df, exception = workflow_instance.execute(data)
            if exception:
                LOGGER.exception(f"Workflow {self.__workflow_name} failed at step {workflow_object.__name__} ", exc_info=exception)
                return WorkflowOutput.failed(df, exception)
            data[WorkflowDataKeys.DATASET] = df

        if self.__cache_manager is not None:
            self.__cache_manager.add_to_cache(df, data[WorkflowDataKeys.IDENTIFIER])

        LOGGER.info(f"Obtained data for {data[WorkflowDataKeys.IDENTIFIER]} online")
        return WorkflowOutput.success(df)
