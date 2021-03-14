""" Test LeagueEndpoint """
import unittest
from unittest.mock import patch
from understatapi.endpoints import LeagueEndpoint, BaseEndpoint


@patch.object(BaseEndpoint, "get_response")
class TestLeagueEndpoint(unittest.TestCase):
    """ Tests for LeagueEndpoint """

    def setUp(self):
        """ setUp """
        self.league = LeagueEndpoint()

    def test_get_data(self, mock_get_response):
        """ test `get_data()` """
        self.league.get_data(league="EPL", season="2019", query="teamsData")
        mock_get_response.assert_called_with(
            url="https://understat.com/league/EPL/2019", query="teamsData"
        )

    def test_get_team_data(self, mock_get_response):
        """ test `get_team_data()` """
        self.league.get_team_data(
            league="EPL", season="2019", element="script"
        )
        mock_get_response.assert_called_with(
            url="https://understat.com/league/EPL/2019",
            query="teamsData",
            element="script",
        )

    def test_get_fixtures(self, mock_get_response):
        """ test `get_fixtures()` """
        self.league.get_fixtures(league="EPL", season="2019", element="script")
        mock_get_response.assert_called_with(
            url="https://understat.com/league/EPL/2019",
            query="datesData",
            element="script",
        )

    def test_getplayer_data(self, mock_get_response):
        """ test `get_player_data()` """
        self.league.get_player_data(
            league="EPL", season="2019", element="script"
        )
        mock_get_response.assert_called_with(
            url="https://understat.com/league/EPL/2019",
            query="playersData",
            element="script",
        )


if __name__ == "__main__":
    unittest.main()
