""" Team parser """
from typing import Dict, Any
from .base import BaseParser


class TeamParser(BaseParser):
    """
    Parse a html page from a url of the form
    ``https://understat.com/team/<team>/<season>``
    """

    def get_player_data(self, html: str) -> Dict[str, Any]:
        """
        Get data on a per-team basis

        :param html: The html string to parse
        """
        return self.parse(html=html, query="playersData")

    def get_match_data(self, html: str) -> Dict[str, Any]:
        """
        Get data on a per match level for a given team in a given season

        :param html: The html string to parse
        """
        return self.parse(html=html, query="datesData")

    def get_context_data(self, html: str) -> Dict[str, Any]:
        """
        Get data based on different contexts in the game

        :param html: The html string to parse
        """
        return self.parse(html=html, query="statisticsData")
