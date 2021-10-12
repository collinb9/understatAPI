""" Match endpoint """
from typing import Dict, Any
import requests
from requests.exceptions import HTTPError
from .base import BaseEndpoint
from ..parsers import MatchParser
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

    parser = MatchParser()

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

    def _get_data(self, **kwargs: str) -> requests.Response:
        """
        Get data on a per-match basis

        :param kwargs: Keyword argument to pass to
            :meth:`understatapi.endpoints.base.BaseEndpoint._request_url`
        """
        if not isinstance(self.match, str):
            raise TypeError("``match`` must be a string")
        self._check_args()
        url = self.base_url + "match/" + self.match

        try:
            response = self._request_url(url=url, **kwargs)
        except HTTPError as err:
            raise InvalidMatch(
                f"{self.match} is not a valid match", match=self.match
            ) from err

        return response

    def get_shot_data(self, **kwargs: str) -> Dict[str, Any]:
        """
        Get shot level data for a match

        :param kwargs: Keyword argument to pass to
            :meth:`understatapi.endpoints.base.BaseEndpoint._get_response`
        """
        res = self._get_data(**kwargs)
        data = self.parser.get_shot_data(html=res.text)
        return data

    def get_roster_data(self, **kwargs: str) -> Dict[str, Any]:
        """
        Get data about the roster for each team

        :param kwargs: Keyword argument to pass to
            :meth:`understatapi.endpoints.base.BaseEndpoint._get_response`
        """
        res = self._get_data(**kwargs)
        data = self.parser.get_roster_data(html=res.text)
        return data

    def get_match_info(self, **kwargs: str) -> Dict[str, Any]:
        """
        Get information about the match

        :param kwargs: Keyword argument to pass to
            :meth:`understatapi.endpoints.base.BaseEndpoint._get_response`
        """
        res = self._get_data(**kwargs)
        data = self.parser.get_match_info(html=res.text)
        return data
