""" Player endpoint """
import pandas as pd
from requests.exceptions import HTTPError
from .base import BaseEndpoint
from ..exceptions import InvalidPlayer


class PlayerEndpoint(BaseEndpoint):
    """
    Use this class to get data from a url of the form
    https://understat.com/player/<player_id>/
    """

    queries = ["matchesData", "shotsData", "groupsData"]

    def get_data(self, player: str, query: str, **kwargs: str) -> pd.DataFrame:
        """
        Get data on a per-player basis

        :param league: str: Understat id of the player to get data for
        :param query: str: Identifies the type of data to get
        :param kwargs: Keyword argument to pass to
            `BaseEndpoint.get_response()`
        """
        self._check_args(query=query)
        url = self.base_url + "player/" + player

        try:
            data = self.get_response(url=url, query=query, **kwargs)
        except HTTPError as err:
            raise InvalidPlayer(player) from err

        return data

    def get_match_data(self, player: str, **kwargs: str) -> pd.DataFrame:
        """
        Get match level data for a player

        :param league: str: Understat id of the player to get data for
        :param kwargs: Keyword argument to pass to
            `BaseEndpoint.get_response()`
        """
        data = self.get_data(player=player, query="matchesData", **kwargs)
        return data

    def get_shot_data(self, player: str, **kwargs: str) -> pd.DataFrame:
        """
        Get shot level data for a player

        :param league: str: Understat id of the player to get data for
        :param kwargs: Keyword argument to pass to
            `BaseEndpoint.get_response()`
        """
        data = self.get_data(player=player, query="shotsData", **kwargs)
        return data

    def get_season_data(self, player: str, **kwargs: str) -> pd.DataFrame:
        """
        Get season level data for a player

        :param league: str: Understat id of the player to get data for
        :param kwargs: Keyword argument to pass to
            `BaseEndpoint.get_response()`
        """
        data = self.get_data(player=player, query="groupsData", **kwargs).T
        return data
