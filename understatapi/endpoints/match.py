""" Match endpoint """
import requests
from requests.exceptions import HTTPError
import pandas as pd
from .base import BaseEndpoint
from ..exceptions import InvalidMatch, PrimaryAttribute


class MatchEndpoint(BaseEndpoint):
    """
    Use this class to get data from a url of the form
    https://understat.com/match/<match_id>
    """

    queries = ["shotsData", "rostersData", "match_info"]

    def __init__(self, match: PrimaryAttribute, session: requests.Session):
        """
        :param match: PrimaryAttribute: Id of match(es) to get data for
        """
        self._primary_attr = match
        super().__init__(primary_attr=self._primary_attr, session=session)

    @property
    def match(self) -> PrimaryAttribute:
        """  match id """
        return self._primary_attr

    def get_data(self, query: str, **kwargs: str) -> pd.DataFrame:
        """
        Get data on a per-match basis

        :param query: str: Identifies the type of data to get,
            one of {shotsData, rostersData, match_info}
        :param kwargs: Keyword argument to pass to
            `BaseEndpoint.get_response()`
        """
        if not isinstance(self.match, str):
            raise TypeError("`match` must be a string")
        self._check_args(query=query)
        url = self.base_url + "match/" + self.match

        try:
            data = self.get_response(url=url, query=query, **kwargs)
        except HTTPError as err:
            raise InvalidMatch(self.match) from err

        return data

    def get_shot_data(self, **kwargs: str) -> pd.DataFrame:
        """
        Get shot level data for a match

        :param kwargs: Keyword argument to pass to
            `BaseEndpoint.get_response()`
        """
        data = self.get_data(query="shotsData", **kwargs).T
        return data

    def get_roster_data(self, **kwargs: str) -> pd.DataFrame:
        """
        Get data about the roster for each team

        :param match: str: Id of match to get data for
        :param kwargs: Keyword argument to pass to
            `BaseEndpoint.get_response()`
        """
        data = self.get_data(query="rostersData", **kwargs).T
        return data

    def get_match_info(self, **kwargs: str) -> pd.DataFrame:
        """
        Get information about the match

        :param match: str: Id of match to get data for
        :param kwargs: Keyword argument to pass to
            `BaseEndpoint.get_response()`
        """
        data = self.get_data(query="match_info", **kwargs).T
        return data
