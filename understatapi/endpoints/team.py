"""Team endpoint"""

from typing import Dict, Any, List
import requests
from requests.exceptions import HTTPError
from .base import BaseEndpoint
from ..parsers import TeamParser
from ..exceptions import InvalidTeam, PrimaryAttribute


class TeamEndpoint(BaseEndpoint):
    """
    Use this class to get data from a url of the form
    ``https://understat.com/team/<team>/<season>``

    :Example:

    .. testsetup::

        import requests
        from understatapi.endpoints import TeamEndpoint

    .. testcleanup::

        session.close()

    .. doctest::

        >>> session = requests.Session()
        >>> team_names = ["Manchester_United", "Liverpool"]
        >>> for team in TeamEndpoint(team_names, session=session):
        ...     print(team.team)
        Manchester_United
        Liverpool

    """

    parser = TeamParser()

    def __init__(self, team: PrimaryAttribute, session: requests.Session) -> None:
        """
        :param team: Name of the team(s) to get data for
        :param session: The current session
        """
        self._primary_attr = team
        super().__init__(primary_attr=self._primary_attr, session=session)

    @property
    def team(self) -> PrimaryAttribute:
        """team name"""
        return self._primary_attr

    def _get_data(self, season: str, **kwargs: Any) -> Dict[str, Any]:
        """
        Get data on a per-team basis via AJAX endpoint.

        :param season: Season to get data for
        :param kwargs: Keyword argument to pass to
            :meth:`understatapi.endpoints.base.BaseEndpoint._request_ajax`
        :return: Dictionary with keys: dates, players, statistics
        """
        if not isinstance(self.team, str):
            raise TypeError("``team`` must be a string")
        self._check_args()
        endpoint = f"getTeamData/{self.team}/{season}"

        try:
            return self._request_ajax(endpoint, **kwargs)
        except HTTPError as err:
            raise InvalidTeam(
                f"{self.team} is not a valid team", team=self.team
            ) from err

    def get_player_data(self, season: str, **kwargs: Any) -> List[Dict[str, Any]]:
        """
        Get data for all players on a given team in a given season

        :param season: Season to get data for
        :param kwargs: Keyword argument to pass to
            :meth:`understatapi.endpoints.base.BaseEndpoint._request_ajax`
        """
        data = self._get_data(season=season, **kwargs)
        return data.get("players", [])

    def get_match_data(self, season: str, **kwargs: Any) -> List[Dict[str, Any]]:
        """
        Get data on a per match level for a given team in a given season

        :param season: Season to get data for
        :param kwargs: Keyword argument to pass to
            :meth:`understatapi.endpoints.base.BaseEndpoint._request_ajax`
        """
        data = self._get_data(season=season, **kwargs)
        return data.get("dates", [])

    def get_context_data(
        self,
        season: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Get data based on different contexts in the game

        :param season: Season to get data for
        :param kwargs: Keyword argument to pass to
            :meth:`understatapi.endpoints.base.BaseEndpoint._request_ajax`
        """
        data = self._get_data(season=season, **kwargs)
        return data.get("statistics", {})
