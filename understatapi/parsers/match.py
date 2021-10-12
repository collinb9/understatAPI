""" Match parser """
from typing import Dict, Any
from .base import BaseParser


class MatchParser(BaseParser):
    """
    Parse a html page from a url of the form
    ``https://understat.com/match/<match_id>``
    """

    def get_shot_data(self, html: str) -> Dict[str, Any]:
        """
        Get shot level data for a match

        :param html: The html string to parse
        """
        return self.parse(html=html, query="shotsData")

    def get_roster_data(self, html: str) -> Dict[str, Any]:
        """
        Get data about the roster for each team

        :param html: The html string to parse
        """
        return self.parse(html=html, query="rostersData")

    def get_match_info(self, html: str) -> Dict[str, Any]:
        """
        Get information about the match

        :param html: The html string to parse
        """
        return self.parse(html=html, query="match_info")
