""" Base endpoint """
from typing import List, Union, Dict, Sequence
import json
import requests
from requests import Response
import pandas as pd
import numpy as np
from numpy.typing import ArrayLike
from ..exceptions import (
    InvalidQuery,
    InvalidLeague,
    InvalidSeason,
    PrimaryAttribute,
)


class BaseEndpoint:
    """
    Base endpoint for understat API

    :base_url: str: The base url to use for requests, `https://understat.com/`
    :leagues: List[str]: The available leagues, `EPL`, `La_Liga`, `Bundesliga`,
        `Serie_A`, `Ligue_1`, `RFPL`
    :queries: List[str]: Strings that can be searched for in the html pages.
    """

    base_url = "https://understat.com/"
    leagues = ["EPL", "La_Liga", "Bundesliga", "Serie_A", "Ligue_1", "RFPL"]
    queries: List[str] = []

    def __init__(
        self,
        primary_attr: PrimaryAttribute,
        session: requests.Session,
    ) -> None:
        """
        Base endpoint for understat API

        :session: requests.Session: The current `request` session
        """
        self.session = session
        self._primary_attr = primary_attr

    def __repr__(self) -> str:
        return "<%s>" % self.__class__.__name__

    def __len__(self) -> int:
        if isinstance(self._primary_attr, str):
            return 1
        if isinstance(self._primary_attr, Sequence):
            return len(self._primary_attr)
        raise TypeError("Primary attribute is not a sequence or string")

    def __getitem__(self, index: int) -> "BaseEndpoint":
        if index >= len(self):
            raise IndexError
        if isinstance(self._primary_attr, str):
            return self.__class__(self._primary_attr, session=self.session)
        return self.__class__(self._primary_attr[index], session=self.session)

    def _check_args(
        self,
        league: str = None,
        season: str = None,
        query: str = None,
    ) -> None:
        """ Handle invalid arguments """
        if league is not None and league not in self.leagues:
            raise InvalidLeague(league)
        if season is not None and int(season) < 2014:
            raise InvalidSeason(season)
        if query is not None and query not in self.queries:
            raise InvalidQuery(query)

    def request_url(self, *args: str, **kwargs: str) -> Response:
        """
        Use the requests module to send a HTTP request to a url, and check
        that this request worked.

        :param args: Arguments to pass to `requests.get()`
        :param kwargs: Keyword arguments to pass to `requests.get()`
        """
        res = self.session.get(*args, **kwargs)
        res.raise_for_status()

        return res

    def extract_data_from_html(
        self,
        html: str,
        query: str = "teamsData",
    ) -> pd.DataFrame:
        """
        Finds a JSON in the HTML according to a query, and returns the
        dictionary corresponding to this JSON.

        :param html: bytes: A html document
        :param query: str: A sub-string to look for in the html document
        """
        # find the query in the html string
        query_index = html.find(query)
        if not query_index > 0:
            raise InvalidQuery(query)
        # get the start and end of the JSON data string
        start = html.find("(", query_index) + 2
        end = html.find(")", start) - 1
        json_data = html[start:end]
        # Clean up the json and return the data
        json_data = json_data.encode("utf8").decode("unicode_escape")
        data = json.loads(json_data)
        data = self.json_to_dataframe(data, orient="index")
        return data

    @staticmethod
    def json_to_dataframe(
        data: Union[List[Dict[str, ArrayLike]], Dict[str, ArrayLike]],
        **kwargs: str,
    ) -> pd.DataFrame:
        """ Convert output of `json.loads()` to a dataframe """
        try:
            data = pd.DataFrame.from_dict(data, **kwargs)
        except AttributeError:
            data = pd.DataFrame(data)
        return data

    @staticmethod
    def try_json_normalize(col: pd.Series) -> pd.DataFrame:
        """
        Try to apply `pd.json_normalize()` to a pd.Series. Otherwise pass
        """
        try:
            keys = col.iloc[0].keys()
            replace_with = {key: np.nan for key in keys}
            col = col.map(lambda x: replace_with if pd.isnull(x) else x)
            col = pd.json_normalize(col).add_prefix(f"{col.name}_")
        except (TypeError, AttributeError):
            col = pd.DataFrame(col)
        return col

    def unpack_dataframe(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Unpack each column in a dataframe whose entries are dictionaries
        into separate columns
        """
        data = pd.concat(
            [self.try_json_normalize(data[col]) for col in data.columns],
            axis=1,
        )
        return data

    def get_response(
        self,
        url: str,
        query: str = "teamsData",
        **kwargs: str,
    ) -> pd.DataFrame:
        """
        Retrieve data from html page

        :param url: str: url to parse
        :param query: str: A sub-string to look for in the html document
        :param kwargs: Keyword arguments to pass to `requests.get()`

        :return: pd.DataFrame: Data retrieved from html page
        """
        res = self.request_url(url, **kwargs)
        data = self.extract_data_from_html(res.text, query=query)

        return data
