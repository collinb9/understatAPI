""" League parser """
from typing import Dict, Any
import json
from .base import BaseParser


class LeagueParser(BaseParser):
    """
    Parse a html page from a url of the form
    ``https://understat.com/league/<league>/<season>``
    """

    def get_team_data(self, html: str) -> Dict[str, Any]:
        """
        Get data for all teams

        :param html: The html string to parse (now JSON from AJAX API)
        """
        # The new API returns JSON directly
        try:
            data = json.loads(html)
            return data.get('teams', {})
        except json.JSONDecodeError:
            # Fallback to old HTML parsing method
            return self.parse(html=html, query="teamsData")

    def get_match_data(self, html: str) -> Dict[str, Any]:
        """
        Get data for all fixtures

        :param html: The html string to parse (now JSON from AJAX API)
        """
        # The new API returns JSON directly
        try:
            data = json.loads(html)
            return data.get('dates', {})
        except json.JSONDecodeError:
            # Fallback to old HTML parsing method
            return self.parse(html=html, query="datesData")

    def get_player_data(self, html: str) -> Dict[str, Any]:
        """
        Get data for all players

        :param html: The html string to parse (now JSON from AJAX API)
        """
        # The new API returns JSON directly
        try:
            data = json.loads(html)
            return data.get('players', {})
        except json.JSONDecodeError:
            # Fallback to old HTML parsing method
            return self.parse(html=html, query="playersData")
