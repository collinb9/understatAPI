""" Test LeagueEndpoint """
import unittest
from unittest.mock import patch
import requests
from understatapi.endpoints import LeagueEndpoint, BaseEndpoint


@patch.object(BaseEndpoint, "get_response")
class TestLeagueEndpoint(unittest.TestCase):
    """ Tests for `LeagueEndpoint` """

    def setUp(self):
        """ setUp """
        self.league = LeagueEndpoint(session=requests.Session())

    def test_get_data(self, mock_get_response):
        """ test `get_data()` """
        self.league.get_data(league="EPL", season="2019", query="teamsData")
        mock_get_response.assert_called_with(
            url="https://understat.com/league/EPL/2019", query="teamsData"
        )

    def test_get_team_data(self, mock_get_response):
        """ test `get_team_data()` """
        self.league.get_team_data(league="EPL", season="2019")
        mock_get_response.assert_called_with(
            url="https://understat.com/league/EPL/2019",
            query="teamsData",
        )

    def test_get_match_data(self, mock_get_response):
        """ test `get_match_data()` """
        self.league.get_match_data(league="EPL", season="2019")
        mock_get_response.assert_called_with(
            url="https://understat.com/league/EPL/2019",
            query="datesData",
        )

    def test_getplayer_data(self, mock_get_response):
        """ test `get_player_data()` """
        self.league.get_player_data(league="EPL", season="2019")
        mock_get_response.assert_called_with(
            url="https://understat.com/league/EPL/2019",
            query="playersData",
        )


class TestLeagueEndpointDunder(unittest.TestCase):
    """ Tests for all `__*__()` methods of `LeagueEndpoint()` """

    def setUp(self):
        """ setUp """
        self.league = LeagueEndpoint(session=requests.Session)

    def test_repr(self):
        """ Test `__repr__()` """
        self.assertEqual(repr(self.league), "<LeagueEndpoint>")


if __name__ == "__main__":
    unittest.main()
