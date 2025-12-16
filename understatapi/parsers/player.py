""" Player parser """
from typing import Dict, Any
import json
from .base import BaseParser


class PlayerParser(BaseParser):
    """
    Parse a html page from a url of the form
    ``https://understat.com/player/<player_id>``
    """

    def get_match_data(self, html: str) -> Dict[str, Any]:
        """
        Get match level data for a player

        :param html: The html string to parse (now JSON from AJAX API)
        """
        try:
            data = json.loads(html)
            return data.get('matches', {})
        except json.JSONDecodeError:
            return self.parse(html=html, query="matchesData")

    def get_shot_data(self, html: str) -> Dict[str, Any]:
        """
        Get shot level data for a player

        :param html: The html string to parse (now JSON from AJAX API)
        """
        try:
            data = json.loads(html)
            return data.get('shots', {})
        except json.JSONDecodeError:
            return self.parse(html=html, query="shotsData")

    def get_season_data(self, html: str) -> Dict[str, Any]:
        """
        Get season level data for a player

        :param html: The html string to parse (now JSON from AJAX API)
        """
        try:
            data = json.loads(html)
            return data.get('statistics', {})
        except json.JSONDecodeError:
            return self.parse(html=html, query="groupsData")
