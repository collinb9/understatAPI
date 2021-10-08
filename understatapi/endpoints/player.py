""" Player endpoint """
from typing import Dict, Any
import requests
from requests.exceptions import HTTPError
from .base import BaseEndpoint
from ..exceptions import InvalidPlayer, PrimaryAttribute


class PlayerEndpoint(BaseEndpoint):
    """
    Use this class to get data from a url of the form
    ``https://understat.com/player/<player_id>/``

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

    queries = ["matchesData", "shotsData", "groupsData"]

    def __init__(
        self, player: PrimaryAttribute, session: requests.Session
    ) -> None:
        """
        :param player: Id of the player(s) to get data for
        :param session: The current session
        """
        self._primary_attr = player
        super().__init__(primary_attr=self._primary_attr, session=session)

    @property
    def player(self) -> PrimaryAttribute:
        """ player id """
        return self._primary_attr

    def _get_data(self, query: str, **kwargs: str) -> Dict[str, Any]:
        """
        Get data on a per-player basis

        :param query: Identifies the type of data to get,
            one of {matchesData, shotsData, groupsData}
        :param kwargs: Keyword argument to pass to
            :meth:`understatapi.endpoints.base.BaseEndpoint._get_response`
        """
        if not isinstance(self.player, str):
            raise TypeError("``player`` must be a string")
        self._check_args()
        url = self.base_url + "player/" + self.player

        try:
            data = self._get_response(url=url, query=query, **kwargs)
        except HTTPError as err:
            raise InvalidPlayer(
                f"{self.player} is not a valid player or player id",
                player=self.player,
            ) from err

        return data

    def get_match_data(self, **kwargs: str) -> Dict[str, Any]:
        """
        Get match level data for a player

        :param kwargs: Keyword argument to pass to
            :meth:`understatapi.endpoints.base.BaseEndpoint._get_response`
        """
        data = self._get_data(query="matchesData", **kwargs)
        return data

    def get_shot_data(self, **kwargs: str) -> Dict[str, Any]:
        """
        Get shot level data for a player

        :param kwargs: Keyword argument to pass to
            :meth:`understatapi.endpoints.base.BaseEndpoint._get_response`
        """
        data = self._get_data(query="shotsData", **kwargs)
        return data

    def get_season_data(self, **kwargs: str) -> Dict[str, Any]:
        """
        Get season level data for a player

        :param kwargs: Keyword argument to pass to
            :meth:`understatapi.endpoints.base.BaseEndpoint._get_response`
        """
        data = self._get_data(query="groupsData", **kwargs)
        return data
