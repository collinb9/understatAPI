"""Base html parser"""
from typing import List
import json
from ..exceptions import (
    InvalidLeague,
    InvalidSeason,
    PrimaryAttribute,
)


class BaseParser:
    """Parse a html document and extract relevant data"""

    queries: List[str]

    # def __init__(self, html: str):
    #     self.html = html

    @staticmethod
    def parse(html: str, query: str = "teamsData"):
        """
        Finds a JSON in the HTML according to a query, and returns the
        object corresponding to this JSON.

        :param html: A html document
        :param query: A sub-string to look for in the html document
        """
        query_index = html.find(query)
        # get the start and end of the JSON data string
        start = html.find("(", query_index) + 2
        end = html.find(")", start) - 1
        json_data = html[start:end]
        # Clean up the json and return the data
        json_data = json_data.encode("utf8").decode("unicode_escape")
        data = json.loads(json_data)
        return data