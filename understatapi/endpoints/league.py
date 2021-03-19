""" League endpoint """
import pandas as pd
from .base import BaseEndpoint


class LeagueEndpoint(BaseEndpoint):
    """
    Endpoint for league data. Use this class to get data from a url of the form
    https://understat.com/league/<league>/<season>
    """

    queries = ["teamsData", "datesData", "playersData"]

    def get_data(
        self, league: str, season: str, query: str, **kwargs: str
    ) -> pd.DataFrame:
        """
        Get data on a league-wide basis

        :param league: str: Name of the league to get data for,
            one of {EPL, La_Liga, Bundesliga, Serie_A, Ligue_1, RFPL}
        :param season: str: Season to get data for
        :param query: str: Identifies the type of data to get,
            one of {teamsData, playersData, datesData}
        :param kwargs: Keyword argument to pass to
            `BaseEndpoint.get_response()`
        """
        self._check_args(league=league, season=season, query=query)
        url = self.base_url + "league/" + league + "/" + season

        data = self.get_response(url=url, query=query, **kwargs)

        return data

    def get_team_data(
        self, league: str, season: str, **kwargs: str
    ) -> pd.DataFrame:
        """
        Get data for all teams in a given league and season

        :param league: str: Name of the league to get data for,
            one of {EPL, La_Liga, Bundesliga, Serie_A, Ligue_1, RFPL}
        :param season: str: Season to get data for
        :param kwargs: Keyword argument to pass to
            `BaseEndpoint.get_response()`
        """
        data = self.get_data(
            league=league, season=season, query="teamsData", **kwargs
        )
        return data

    def get_match_data(
        self, league: str, season: str, **kwargs: str
    ) -> pd.DataFrame:
        """
        Get data for all fixtures in a given league and season.

        :param league: str: Name of the league to get data for,
            one of {EPL, La_Liga, Bundesliga, Serie_A, Ligue_1, RFPL}
        :param season: str: Season to get data for
        :param kwargs: Keyword argument to pass to
            `BaseEndpoint.get_response()`
        """
        data = self.get_data(
            league=league, season=season, query="datesData", **kwargs
        )
        return data

    def get_player_data(
        self, league: str, season: str, **kwargs: str
    ) -> pd.DataFrame:
        """
        Get data for all players in a given league and season

        :param league: str: Name of the league to get data for,
            one of {EPL, La_Liga, Bundesliga, Serie_A, Ligue_1, RFPL}
        :param season: str: Season to get data for
        :param kwargs: Keyword argument to pass to
            `BaseEndpoint.get_response()`
        """
        data = self.get_data(
            league=league, season=season, query="playersData", **kwargs
        )
        return data
