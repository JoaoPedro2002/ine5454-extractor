from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from abc import ABC, abstractmethod

from src.workflow.workflow import WorkflowDataKeys
from src.workflow.workflow_object import WorkflowObject, WorkflowExecutionStatus


class Parser(WorkflowObject, ABC):
    """
    Abstract class for parsers that parse data from an url and return a pandas dataframe
    This is supposed to be the first step in a workflow
    """

    def execute(self, data: dict) -> tuple[WorkflowExecutionStatus, pd.DataFrame | None]:
        try:
            df = self.parse(data[WorkflowDataKeys.IDENTIFIER])
        except Exception:
            return WorkflowExecutionStatus.FAILED, None
        return WorkflowExecutionStatus.SUCCESS, df

    def parse(self, identifier: str) -> pd.DataFrame:
        html = urlopen(self.get_url() % identifier)
        soup = BeautifulSoup(html, features="html.parser")
        headers = self.parse_headers(soup)
        rows_data = self.parse_row_data(soup)

        df = pd.DataFrame(rows_data, columns=headers)
        # remove empty columns
        try:
            df.drop([""], axis=1, inplace=True)
        except KeyError:
            pass
        return df

    @abstractmethod
    def parse_row_data(self, soup: BeautifulSoup) -> list[list[str]]:
        raise NotImplementedError("This method must be implemented by subclasses")

    @abstractmethod
    def parse_headers(self, soup: BeautifulSoup) -> list[str]:
        raise NotImplementedError("This method must be implemented by subclasses")

    @abstractmethod
    def get_url(self) -> str:
        raise NotImplementedError("This method must be implemented by subclasses")

    @abstractmethod
    def get_cache_subdir(self) -> str:
        raise NotImplementedError("This method must be implemented by subclasses")