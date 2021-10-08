""" Match endpoint """
from typing import Dict, Any
import requests
from requests.exceptions import HTTPError
from .base import BaseEndpoint
from ..exceptions import InvalidMatch, PrimaryAttribute


class MatchEndpoint(BaseEndpoint):
    """
    Use this class to get data from a url of the form
    ``https://understat.com/match/<match_id>``

    :Example:

    .. testsetup::

        import requests
        from understatapi.endpoints import MatchEndpoint

    .. testcleanup::

        session.close()

    .. doctest::

        >>> session = requests.Session()
        >>> match_ids = ["123", "456"]
        >>> for match in MatchEndpoint(match_ids, session=session):
        ...     print(match.match)
        123
        456
    """

    queries = ["shotsData", "rostersData", "match_info"]

    def __init__(self, match: PrimaryAttribute, session: requests.Session):
        """
        :param match: Id of match(es) to get data for
        :param session: The current session
        """
        self._primary_attr = match
        super().__init__(primary_attr=self._primary_attr, session=session)

    @property
    def match(self) -> PrimaryAttribute:
        """  match id """
        return self._primary_attr

    def _get_data(self, query: str, **kwargs: str) -> Dict[str, Any]:
        """
        Get data on a per-match basis

        :param query: Identifies the type of data to get,
            one of {shotsData, rostersData, match_info}
        :param kwargs: Keyword argument to pass to
            :meth:`understatapi.endpoints.base.BaseEndpoint._get_response`
        """
        if not isinstance(self.match, str):
            raise TypeError("``match`` must be a string")
        self._check_args()
        url = self.base_url + "match/" + self.match

        try:
            data = self._get_response(url=url, query=query, **kwargs)
        except HTTPError as err:
            raise InvalidMatch(
                f"{self.match} is not a valid match", match=self.match
            ) from err

        return data

    def get_shot_data(self, **kwargs: str) -> Dict[str, Any]:
        """
        Get shot level data for a match

        :param kwargs: Keyword argument to pass to
            :meth:`understatapi.endpoints.base.BaseEndpoint._get_response`
        """
        data = self._get_data(query="shotsData", **kwargs)
        return data

    def get_roster_data(self, **kwargs: str) -> Dict[str, Any]:
        """
        Get data about the roster for each team

        :param kwargs: Keyword argument to pass to
            :meth:`understatapi.endpoints.base.BaseEndpoint._get_response`
        """
        data = self._get_data(query="rostersData", **kwargs)
        return data

    def get_match_info(self, **kwargs: str) -> Dict[str, Any]:
        """
        Get information about the match

        :param kwargs: Keyword argument to pass to
            :meth:`understatapi.endpoints.base.BaseEndpoint._get_response`
        """
        data = self._get_data(query="match_info", **kwargs)
        return data
