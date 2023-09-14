from src.cache_manager import CacheManager
from src.normalizer.player_id_normalizer import PlayerIdNormalizer
from src.normalizer.teammates_normalizer import TeammatesNormalizer
from src.parsers.player_id_parser import PlayerIdParser
from src.parsers.teammates_parser import TeammatesParser
from src.workflow.workflow import Workflow, WorkflowDataKeys


# class WorkflowNode:
#     def __init__(self, workflow: Workflow, operation: str):
#         self.workflow = workflow
#         self.children = []
#         self.operation = operation


class Extractor:
    def __init__(self):
        # self.__workflows = []
        # self.__steps = []
        # self.__data = None
        # self.__pointer = None
        pass

    @staticmethod
    def extract():
        player_workflow = Workflow("Players", "NBA Players workflow",
                             [PlayerIdParser, PlayerIdNormalizer],
                             cache_manager=CacheManager(CacheManager.PLAYER_ID_CACHE_SUBDIR))
        players = []
        for letter in "abcdefghijklmnopqrstuvwxyz":
            df = player_workflow.execute({WorkflowDataKeys.IDENTIFIER: letter})
            players.extend(df["id"].tolist())

        print("Total number of players: {}".format(len(players)))

        teammates_workflow = Workflow("Teammates", "NBA Teammates workflow",
                                      [TeammatesParser, TeammatesNormalizer],
                                      cache_manager=CacheManager(CacheManager.TEAMMATES_CACHE_SUBDIR))

        max_players = 10

        i = 0
        for player in players:
            if i == max_players:
                break
            i += 1
            df = teammates_workflow.execute({WorkflowDataKeys.IDENTIFIER: player})

