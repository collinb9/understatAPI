""" Player endpoint """
import requests
import pandas as pd
from requests.exceptions import HTTPError
from .base import BaseEndpoint
from ..exceptions import InvalidPlayer, PrimaryAttribute


class PlayerEndpoint(BaseEndpoint):
    """
    Use this class to get data from a url of the form
    https://understat.com/player/<player_id>/
    """

    queries = ["matchesData", "shotsData", "groupsData"]

    def __init__(
        self, player: PrimaryAttribute, session: requests.Session
    ) -> None:
        """
        :param player: PrimaryAttribute: Understat id of the player(s)
            to get data for
        :session: requests.Session: The current session
        """
        self._primary_attr = player
        super().__init__(primary_attr=self._primary_attr, session=session)

    @property
    def player(self) -> PrimaryAttribute:
        """ player id """
        return self._primary_attr

    def get_data(self, query: str, **kwargs: str) -> pd.DataFrame:
        """
        Get data on a per-player basis

        :param query: str: Identifies the type of data to get,
            one of {matchesData, shotsData, groupsData}
        :param kwargs: Keyword argument to pass to
            `BaseEndpoint.get_response()`
        """
        if not isinstance(self.player, str):
            raise TypeError("`player` must be a string")
        self._check_args(query=query)
        url = self.base_url + "player/" + self.player

        try:
            data = self.get_response(url=url, query=query, **kwargs)
        except HTTPError as err:
            raise InvalidPlayer(self.player) from err

        return data

    def get_match_data(self, **kwargs: str) -> pd.DataFrame:
        """
        Get match level data for a player

        :param kwargs: Keyword argument to pass to
            `BaseEndpoint.get_response()`
        """
        data = self.get_data(query="matchesData", **kwargs)
        return data

    def get_shot_data(self, **kwargs: str) -> pd.DataFrame:
        """
        Get shot level data for a player

        :param kwargs: Keyword argument to pass to
            `BaseEndpoint.get_response()`
        """
        data = self.get_data(query="shotsData", **kwargs)
        return data

    def get_season_data(self, **kwargs: str) -> pd.DataFrame:
        """
        Get season level data for a player

        :param league: str: Understat id of the player to get data for
        :param kwargs: Keyword argument to pass to
            `BaseEndpoint.get_response()`
        """
        data = self.get_data(query="groupsData", **kwargs).T
        return data
