""" Match endpoint """
from requests.exceptions import HTTPError
import pandas as pd
from .base import BaseEndpoint
from ..exceptions import InvalidMatch


class MatchEndpoint(BaseEndpoint):
    """
    Use this class to get data from a url of the form
    https://understat.com/match/<match_id>
    """

    queries = ["shotsData", "rostersData", "match_info", "PROMOTION"]

    def get_data(self, match: str, query: str, **kwargs: str) -> pd.DataFrame:
        """
        Get data on a per-match basis

        :param match: str: Id of match to get data for
        :param query: str: Identifies the type of data to get
        :param kwargs: Keyword argument to pass to
            `BaseEndpoint.get_response()`
        """
        self._check_args(query=query)
        url = self.base_url + "match/" + match

        try:
            data = self.get_response(url=url, query=query, **kwargs)
        except HTTPError as err:
            raise InvalidMatch(match) from err

        return data

    def get_shot_data(self, match: str, **kwargs: str) -> pd.DataFrame:
        """
        Get shot level data for a match

        :param match: str: Id of match to get data for
        :param kwargs: Keyword argument to pass to
            `BaseEndpoint.get_response()`
        """
        data = self.get_data(match=match, query="shotsData", **kwargs).T
        return data

    def get_roster_data(self, match: str, **kwargs: str) -> pd.DataFrame:
        """
        Get data about the roster for each team

        :param match: str: Id of match to get data for
        :param kwargs: Keyword argument to pass to
            `BaseEndpoint.get_response()`
        """
        data = self.get_data(match=match, query="rostersData", **kwargs).T
        return data

    def get_match_info(self, match: str, **kwargs: str) -> pd.DataFrame:
        """
        Get information about the match

        :param match: str: Id of match to get data for
        :param kwargs: Keyword argument to pass to
            `BaseEndpoint.get_response()`
        """
        data = self.get_data(match=match, query="match_info", **kwargs).T
        return data
