# pylint: disable=duplicate-code
# pylint: disable=unused-argument
""" Test LeagueEndpoint """
import unittest
from unittest.mock import patch
import requests
from understatapi.endpoints import LeagueEndpoint, BaseEndpoint


@patch.object(BaseEndpoint, "get_response")
class TestLeagueEndpoint(unittest.TestCase):
    """ Tests for `LeagueEndpoint` """

    def setUp(self):
        self.league = LeagueEndpoint(league="EPL", session=requests.Session())

    def tearDown(self):
        self.league.session.close()

    def test_get_data(self, mock_get_response):
        """ test `get_data()` """
        self.league.get_data(season="2019", query="teamsData")
        mock_get_response.assert_called_with(
            url="https://understat.com/league/EPL/2019", query="teamsData"
        )

    def test_get_team_data(self, mock_get_response):
        """ test `get_team_data()` """
        self.league.get_team_data(season="2019")
        mock_get_response.assert_called_with(
            url="https://understat.com/league/EPL/2019",
            query="teamsData",
        )

    def test_get_match_data(self, mock_get_response):
        """ test `get_match_data()` """
        self.league.get_match_data(season="2019")
        mock_get_response.assert_called_with(
            url="https://understat.com/league/EPL/2019",
            query="datesData",
        )

    def test_getplayer_data(self, mock_get_response):
        """ test `get_player_data()` """
        self.league.get_player_data(season="2019")
        mock_get_response.assert_called_with(
            url="https://understat.com/league/EPL/2019",
            query="playersData",
        )

    def test_get_data_type_error(self, mock_get_response):
        """
        test that `get_data()` raises a TypeError
        when `league` is not a string
        """
        self.league._primary_attr = None
        with self.assertRaises(TypeError):
            _ = self.league.get_data(season="", query="")


class TestLeagueEndpointDunder(unittest.TestCase):
    """ Tests for all `__*__()` methods of `LeagueEndpoint()` """

    def setUp(self):
        self.league = LeagueEndpoint("EPL", session=requests.Session())

    def tearDown(self):
        self.league.session.close()

    def test_init(self):
        """ Test `__init__()` """
        with self.subTest(test="primary_attr"):
            self.assertEqual(self.league._primary_attr, "EPL")
        with self.subTest(test="player"):
            self.assertEqual(self.league.league, "EPL")
        with self.subTest(test="session"):
            self.assertIsInstance(self.league.session, requests.Session)

    def test_repr(self):
        """ Test `__repr__()` """
        self.assertEqual(repr(self.league), "<LeagueEndpoint>")


if __name__ == "__main__":
    unittest.main()
