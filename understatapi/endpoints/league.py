""" League endpoint """
from typing import Dict, Any
import requests
from .base import BaseEndpoint
from ..parsers import LeagueParser
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

    parser = LeagueParser()

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

    def _get_data(self, season: str, **kwargs: str) -> requests.Response:
        """
        Get data on a league-wide basis

        :param season: Season to get data for
        :param kwargs: Keyword argument to pass to
            :meth:`understatapi.endpoints.base.BaseEndpoint._request_url`
        """
        if not isinstance(self.league, str):
            raise TypeError("``league`` must be a string")
        self._check_args(league=self.league, season=season)
        url = self.base_url + "league/" + self.league + "/" + season

        response = self._request_url(url=url, **kwargs)

        return response

    def get_team_data(self, season: str, **kwargs: str) -> Dict[str, Any]:
        """
        Get data for all teams in a given league and season

        :param season: Season to get data for
        :param kwargs: Keyword argument to pass to
            :meth:`understatapi.endpoints.base.BaseEndpoint._get_response`
        """
        res = self._get_data(season=season, **kwargs)
        data = self.parser.get_team_data(html=res.text)
        return data

    def get_match_data(self, season: str, **kwargs: str) -> Dict[str, Any]:
        """
        Get data for all fixtures in a given league and season.

        :param season: Season to get data for
        :param kwargs: Keyword argument to pass to
            :meth:`understatapi.endpoints.base.BaseEndpoint._get_response`
        """
        res = self._get_data(season=season, **kwargs)
        data = self.parser.get_match_data(html=res.text)
        return data

    def get_player_data(self, season: str, **kwargs: str) -> Dict[str, Any]:
        """
        Get data for all players in a given league and season

        :param season: Season to get data for
        :param kwargs: Keyword argument to pass to
            :meth:`understatapi.endpoints.base.BaseEndpoint._get_response()`
        """
        res = self._get_data(season=season, **kwargs)
        data = self.parser.get_player_data(html=res.text)
        return data
