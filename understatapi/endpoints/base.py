""" Base endpoint """
from typing import List, Union, Dict
import json
import requests
from requests import Response
import pandas as pd
from numpy.typing import ArrayLike
from bs4 import BeautifulSoup
from ..exceptions import (
    InvalidQuery,
    InvalidLeague,
    InvalidSeason,
)


class BaseEndpoint:
    """Base endpoint for understat API"""

    base_url = "https://understat.com/"
    leagues = ["EPL", "La_Liga", "Bundesliga", "Serie_A", "Ligue_1", "RFPL"]
    queries: List[str] = []

    def __repr__(self) -> str:
        return "<%s>" % self.__class__.__name__

    def _check_args(
        self, league: str = None, season: str = None, query: str = None
    ) -> None:
        """ Handle invalid arguments """
        if league is not None and league not in self.leagues:
            raise InvalidLeague(league)
        if season is not None and int(season) < 2014:
            raise InvalidSeason(season)
        if query is not None and query not in self.queries:
            raise InvalidQuery(query)

    @staticmethod
    def request_url(*args: str, **kwargs: str) -> Response:
        """
        Use the requests module to send a HTTP request to a url, and check
        that this request worked.

        :param *args: Arguments to pass to `requests.get()`
        :param **kwargs: Keyword arguments to pass to `requests.get()`
        """
        res = requests.get(*args, **kwargs)
        res.raise_for_status()

        return res

    def extract_data_from_html(
        self,
        soup: BeautifulSoup,
        element: str = "script",
        query: str = "teamsData",
    ) -> pd.DataFrame:
        """
        Finds a JSON in the HTML according to a query, and returns the dictionary
        corresponding to this JSON.

        :param soup: BeautifulSoup: BeautifulSoup object to be parsed
        :param element: str: HTML element to find. Passed to `bs4.BeautifulSoup.find()`
        :param query: Tuple[str, str]: Identifies the particular element that contains
            the relevant data
        """
        result = soup.find_all(element)
        # Get the part of the HTML that contains the script we are looking for
        string_with_json_obj = None
        for elem in result:
            # elem.text should work instead of str(elem)
            if query in str(elem):
                string_with_json_obj = str(elem).strip()
        if string_with_json_obj is None:
            raise InvalidQuery(query)
        # Extract the json string
        start = string_with_json_obj.index("('") + 2
        end = string_with_json_obj.index("')")
        json_data = string_with_json_obj[start:end]
        # Clean up the json and return the data
        json_data = json_data.encode("utf8").decode("unicode_escape")
        data = json.loads(json_data)
        data = self.json_to_dataframe(data, orient="index")
        return data

    @staticmethod
    def json_to_dataframe(
        data: Union[List[Dict[str, ArrayLike]], Dict[str, ArrayLike]],
        **kwargs: str
    ) -> pd.DataFrame:
        """ Convert output of `json.loads()` to a dataframe """
        try:
            data = pd.DataFrame.from_dict(data, **kwargs)
        except AttributeError:
            data = pd.DataFrame(data)
        return data

    def get_response(
        self,
        url: str,
        element: str = "script",
        query: str = "teamsData",
        **kwargs: str
    ) -> pd.DataFrame:
        """
        Retrieve data from html page

        :param url: str: url to parse
        :param element: str: HTML element to find. Passed to `bs4.BeautifulSoup.find()`
        :param query: Tuple[str, str]: Identifies the particular element that contains
            the relevant data
        :param kwargs: Keyword arguments to pass to `requuests.get()`

        :return: pd.DataFrame: Data retrieved from html page
        """
        res = self.request_url(url, **kwargs)
        soup = BeautifulSoup(res.content, "lxml")
        data = self.extract_data_from_html(soup, element=element, query=query)

        return data
