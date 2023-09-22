import time

from src.cache_manager import CacheManager
from src.logger import LOGGER
from src.normalizer.player_id_normalizer import PlayerIdNormalizer
from src.normalizer.teammates_normalizer import TeammatesNormalizer
from src.parsers.player_id_parser import PlayerIdParser
from src.parsers.teammates_parser import TeammatesParser
from src.workflow.workflow import Workflow, WorkflowDataKeys
from src.workflow.workflow_output import WorkflowOutput


class Extractor:
    def __init__(self):
        pass

    @staticmethod
    def extract(request_timeout: int = 10):
        players = Extractor.__extract_players(request_timeout)

        # max_players = 10
        Extractor.__extract_teammates(players, request_timeout)

        LOGGER.info("End of extraction")

    @staticmethod
    def __extract_teammates(players, request_timeout, max_players=-1):
        if max_players == -1:
            max_players = len(players)

        teammates_workflow = Workflow("Teammates", "NBA Teammates workflow",
                                      [TeammatesParser, TeammatesNormalizer],
                                      cache_manager=CacheManager(CacheManager.TEAMMATES_CACHE_SUBDIR),
                                      parse_already_in_cache=False)
        i = 0
        for player in players:
            if i == max_players:
                break
            out = teammates_workflow.execute({WorkflowDataKeys.IDENTIFIER: player})
            Extractor.__handle_output(out, request_timeout)
            if out.online:
                i += 1

    @staticmethod
    def __extract_players(request_timeout):
        player_workflow = Workflow("Players", "NBA Players workflow",
                                   [PlayerIdParser, PlayerIdNormalizer],
                                   cache_manager=CacheManager(CacheManager.PLAYER_ID_CACHE_SUBDIR))
        players = []
        for letter in "abcdefghijklmnopqrstuvwxyz":
            out = player_workflow.execute({WorkflowDataKeys.IDENTIFIER: letter})
            Extractor.__handle_output(out, request_timeout)
            players.extend(out.df["id"].tolist())
        LOGGER.debug("Total number of players: {}".format(len(players)))
        return players

    @staticmethod
    def __handle_output(out: WorkflowOutput, request_timeout):
        if out.exception:
            exit(1)
        if out.online:
            LOGGER.debug("Sleeping for {} seconds".format(request_timeout))
            time.sleep(request_timeout)
