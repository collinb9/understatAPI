""" League endpoint """
from typing import Dict, Any
import requests
from .base import BaseEndpoint
from ..exceptions import PrimaryAttribute


class LeagueEndpoint(BaseEndpoint):
    """#pylint: disable-line-too-long
    Endpoint for league data. Use this class to get data from a url of the form
    ``https://understat.com/league/<league>/<season>``

    :Example:

    .. testsetup::

        import requests
        from understatapi.endpoints import LeagueEndpoint

    .. testcleanup::

        session.close()

    .. doctest::

        >>> session = requests.Session()
        >>> leagues = ["EPL", "Bundesliga"]
        >>> for league in LeagueEndpoint(leagues, session=session):
        ...     print(league.league)
        EPL
        Bundesliga

    """

    queries = ["teamsData", "datesData", "playersData"]

    def __init__(self, league: PrimaryAttribute, session: requests.Session):
        """
        :param league: Name of the league(s) to get data for,
            one of {EPL, La_Liga, Bundesliga, Serie_A, Ligue_1, RFPL}
        :param session: The current session
        """
        self._primary_attr = league
        super().__init__(primary_attr=self._primary_attr, session=session)

    @property
    def league(self) -> PrimaryAttribute:
        """ league name """
        return self._primary_attr

    def _get_data(
        self, season: str, query: str, **kwargs: str
    ) -> Dict[str, Any]:
        """
        Get data on a league-wide basis

        :param season: Season to get data for
        :param query: Identifies the type of data to get,
            one of {teamsData, playersData, datesData}
        :param kwargs: Keyword argument to pass to
            :meth:`understatapi.endpoints.base.BaseEndpoint._get_response`
        """
        if not isinstance(self.league, str):
            raise TypeError("``league`` must be a string")
        self._check_args(league=self.league, season=season)
        url = self.base_url + "league/" + self.league + "/" + season

        data = self._get_response(url=url, query=query, **kwargs)

        return data

    def get_team_data(self, season: str, **kwargs: str) -> Dict[str, Any]:
        """
        Get data for all teams in a given league and season

        :param season: Season to get data for
        :param kwargs: Keyword argument to pass to
            :meth:`understatapi.endpoints.base.BaseEndpoint._get_response`
        """
        data = self._get_data(season=season, query="teamsData", **kwargs)
        return data

    def get_match_data(self, season: str, **kwargs: str) -> Dict[str, Any]:
        """
        Get data for all fixtures in a given league and season.

        :param season: Season to get data for
        :param kwargs: Keyword argument to pass to
            :meth:`understatapi.endpoints.base.BaseEndpoint._get_response`
        """
        data = self._get_data(season=season, query="datesData", **kwargs)
        return data

    def get_player_data(self, season: str, **kwargs: str) -> Dict[str, Any]:
        """
        Get data for all players in a given league and season

        :param season: Season to get data for
        :param kwargs: Keyword argument to pass to
            :meth:`understatapi.endpoints.base.BaseEndpoint._get_response()`
        """
        data = self._get_data(season=season, query="playersData", **kwargs)
        return data
