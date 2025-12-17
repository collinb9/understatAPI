"""Player endpoint"""

from typing import Dict, Any, List
import requests
from requests.exceptions import HTTPError
from .base import BaseEndpoint
from ..parsers import PlayerParser
from ..exceptions import InvalidPlayer, PrimaryAttribute


class PlayerEndpoint(BaseEndpoint):
    """
    Use this class to get data from a url of the form
    ``https://understat.com/player/<player_id>``

    :Example:

    .. testsetup::

        import requests
        from understatapi.endpoints import PlayerEndpoint

    .. testcleanup::

        session.close()

    .. doctest::

        >>> session = requests.Session()
        >>> player_ids = ["000", "111"]
        >>> for player in PlayerEndpoint(player_ids, session=session):
        ...     print(player.player)
        000
        111

    """

    parser = PlayerParser()

    def __init__(self, player: PrimaryAttribute, session: requests.Session) -> None:
        """
        :param player: Id of the player(s) to get data for
        :param session: The current session
        """
        self._primary_attr = player
        super().__init__(primary_attr=self._primary_attr, session=session)

    @property
    def player(self) -> PrimaryAttribute:
        """player id"""
        return self._primary_attr

    def _get_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Get data on a per-player basis via AJAX endpoint.

        :param kwargs: Keyword argument to pass to
            :meth:`understatapi.endpoints.base.BaseEndpoint._request_ajax`
        :return: Dictionary with keys: player, matches, shots, groups, etc.
        """
        if not isinstance(self.player, str):
            raise TypeError("``player`` must be a string")
        self._check_args()
        endpoint = f"getPlayerData/{self.player}"

        try:
            return self._request_ajax(endpoint, **kwargs)
        except HTTPError as err:
            raise InvalidPlayer(
                f"{self.player} is not a valid player or player id",
                player=self.player,
            ) from err

    def get_match_data(self, **kwargs: Any) -> List[Dict[str, Any]]:
        """
        Get match level data for a player

        :param kwargs: Keyword argument to pass to
            :meth:`understatapi.endpoints.base.BaseEndpoint._request_ajax`
        """
        data = self._get_data(**kwargs)
        return data.get("matches", [])

    def get_shot_data(self, **kwargs: Any) -> List[Dict[str, Any]]:
        """
        Get shot level data for a player

        :param kwargs: Keyword argument to pass to
            :meth:`understatapi.endpoints.base.BaseEndpoint._request_ajax`
        """
        data = self._get_data(**kwargs)
        return data.get("shots", [])

    def get_season_data(self, **kwargs: Any) -> List[Dict[str, Any]]:
        """
        Get season level data for a player

        :param kwargs: Keyword argument to pass to
            :meth:`understatapi.endpoints.base.BaseEndpoint._request_ajax`
        """
        data = self._get_data(**kwargs)
        return data.get("groups", [])
