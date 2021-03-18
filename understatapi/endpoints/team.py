""" Team endpoint """
from requests.exceptions import HTTPError
import pandas as pd
from .base import BaseEndpoint
from ..exceptions import InvalidTeam


class TeamEndpoint(BaseEndpoint):
    """
    Use this class to get data from a url of the form
    https://understat.com/team/<team>/<season>
    """

    queries = ["datesData", "statisticsData", "playersData"]

    def get_data(
        self, team: str, season: str, query: str, **kwargs: str
    ) -> pd.DataFrame:
        """
        Get data on a per-player basis

        :param team: str: Name of the team to get data for
        :param season: str: Season to get data for
        :param query: str: Identifies the type of data to get
        :param kwargs: Keyword argument to pass to
            `BaseEndpoint.get_response()`
        """
        self._check_args(query=query)
        url = self.base_url + "team/" + team + "/" + season

        try:
            data = self.get_response(url=url, query=query, **kwargs)
        except HTTPError as err:
            raise InvalidTeam(team) from err

        return data

    def get_player_data(
        self, team: str, season: str, **kwargs: str
    ) -> pd.DataFrame:
        """
        Get data for all players on a given team for a season

        :param team: str: Name of the team to get data for
        :param season: str: Season to get data for
        :param kwargs: Keyword argument to pass to
            `BaseEndpoint.get_response()`
        """
        data = self.get_data(
            team=team, season=season, query="playersData", **kwargs
        )
        return data

    def get_match_data(
        self, team: str, season: str, **kwargs: str
    ) -> pd.DataFrame:
        """
        Get data on a per player level for a given team

        :param team: str: Name of the team to get data for
        :param season: str: Season to get data for
        :param kwargs: Keyword argument to pass to
            `BaseEndpoint.get_response()`
        """
        data = self.get_data(
            team=team, season=season, query="datesData", **kwargs
        )
        return data

    def get_context_data(
        self,
        team: str,
        season: str,
        **kwargs: str,
    ) -> pd.DataFrame:
        """
        Get data based on different contexts in the game

        :param team: str: Name of the team to get data for
        :param season: str: Season to get data for
        :param kwargs: Keyword argument to pass to
            ``BaseEndpoint.get_response()``
        :return: pd.DataFrame: A dataframe with 6 column, each of which
            relates to a different context int the game. The below tables
            show the dataframe that you get if you set ``unpack=True`` for
            each column, i.e. ``get_context_data(team="Manchester_United",
            season="2019"``, unpack=True, context="situation") would return
            a dataframe with the rows shown in the first table.
        """
        data = self.get_data(
            team=team, season=season, query="statisticsData", **kwargs
        ).T
        return data
