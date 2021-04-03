""" Team endpoint """
import requests
from requests.exceptions import HTTPError
import pandas as pd
from .base import BaseEndpoint
from ..exceptions import InvalidTeam, PrimaryAttribute


class TeamEndpoint(BaseEndpoint):
    """
    Use this class to get data from a url of the form
    https://understat.com/team/<team>/<season>
    """

    queries = ["datesData", "statisticsData", "playersData"]

    def __init__(
        self, team: PrimaryAttribute, session: requests.Session
    ) -> None:
        """
        :param team: PrimaryAttribute: Name of the team(s) to get data for
        :session: requests.Session: The current session
        """
        self._primary_attr = team
        super().__init__(primary_attr=self._primary_attr, session=session)

    @property
    def team(self) -> PrimaryAttribute:
        """ team name """
        return self._primary_attr

    def get_data(self, season: str, query: str, **kwargs: str) -> pd.DataFrame:
        """
        Get data on a per-team basis

        :param season: str: Season to get data for
        :param query: str: Identifies the type of data to get,
            one of {playersData, statisticsData, datesData}
        :param kwargs: Keyword argument to pass to
            `BaseEndpoint.get_response()`
        """
        if not isinstance(self.team, str):
            raise TypeError("`team` must be a string")
        self._check_args(query=query)
        url = self.base_url + "team/" + self.team + "/" + season

        try:
            data = self.get_response(url=url, query=query, **kwargs)
        except HTTPError as err:
            raise InvalidTeam(self.team) from err

        return data

    def get_player_data(self, season: str, **kwargs: str) -> pd.DataFrame:
        """
        Get data for all players on a given team in a given season

        :param season: str: Season to get data for
        :param kwargs: Keyword argument to pass to
            `BaseEndpoint.get_response()`
        """
        data = self.get_data(season=season, query="playersData", **kwargs)
        return data

    def get_match_data(self, season: str, **kwargs: str) -> pd.DataFrame:
        """
        Get data on a per match level for a given team in a given season

        :param season: str: Season to get data for
        :param kwargs: Keyword argument to pass to
            `BaseEndpoint.get_response()`
        """
        data = self.get_data(season=season, query="datesData", **kwargs)
        return data

    def get_context_data(
        self,
        season: str,
        **kwargs: str,
    ) -> pd.DataFrame:
        """
        Get data based on different contexts in the game

        :param season: str: Season to get data for
        :param kwargs: Keyword argument to pass to
            ``BaseEndpoint.get_response()``
        """
        data = self.get_data(season=season, query="statisticsData", **kwargs).T
        return data
