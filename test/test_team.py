# pylint: disable=unused-argument
# pylint: disable=duplicate-code
""" Test TeamEndpoint """
import unittest
from unittest.mock import patch
from test import mocked_requests_get, assert_data_equal
import requests
import pandas as pd
from understatapi.endpoints import TeamEndpoint, BaseEndpoint
from understatapi.exceptions import InvalidTeam


@patch.object(BaseEndpoint, "request_url")
@patch.object(requests.Session, "get", side_effect=mocked_requests_get)
class TestTeamEndpoint(unittest.TestCase):
    """ Tests for `TeamEndpoint` """

    def setUp(self):
        """ setUp """
        self.team = TeamEndpoint(session=requests.Session())
        self.base = BaseEndpoint(session=requests.Session())

    def test_get_player_data_return_value(self, mock_get, mock_request_url):
        """ test `get_match_data()` """
        mock_request_url.return_value = mocked_requests_get(
            "test/resources/team.html"
        )
        data = self.team.get_player_data(
            team="Manchester_United", season="2019"
        )
        expected_data = pd.read_csv(
            "test/resources/data/team_playersdata.csv", index_col=0
        )
        assert_data_equal(data, expected_data)

    @patch.object(BaseEndpoint, "get_response")
    def test_get_player_data_args(
        self, mock_get_response, mock_get, mock_request_url
    ):
        """ test `get_player_data()` """
        self.team.get_player_data(team="Manchester_United", season="2019")
        mock_get_response.assert_called_with(
            url="https://understat.com/team/Manchester_United/2019",
            query="playersData",
        )

    def test_get_match_data_return_value(self, mock_get, mock_request_url):
        """ test `get_match_data()` """
        mock_request_url.return_value = mocked_requests_get(
            "test/resources/team.html"
        )
        data = self.team.get_match_data(
            team="Manchester_United", season="2019"
        )
        data = self.base.unpack_dataframe(data)
        expected_data = pd.read_csv(
            "test/resources/data/team_datesdata.csv", index_col=0
        )
        assert_data_equal(data, expected_data)

    @patch.object(BaseEndpoint, "get_response")
    def test_get_match_data_args(
        self, mock_get_response, mock_get, mock_request_url
    ):
        """ test `get_match_data()` """
        self.team.get_match_data(team="Manchester_United", season="2019")
        mock_get_response.assert_called_with(
            url="https://understat.com/team/Manchester_United/2019",
            query="datesData",
        )

    def test_get_context_data_return_value(self, mock_get, mock_request_url):
        """ test `get_context_data()` """
        mock_request_url.return_value = mocked_requests_get(
            "test/resources/team.html"
        )
        data = self.team.get_context_data(
            team="Manchester_United", season="2019"
        )
        data = self.base.unpack_dataframe(data)
        expected_data = pd.read_csv(
            "test/resources/data/team_statisticsdata.csv", index_col=0
        )
        assert_data_equal(data, expected_data)

    @patch.object(BaseEndpoint, "get_response")
    def test_get_context_data_args(
        self, mock_get_response, mock_get, mock_request_url
    ):
        """ test `get_match_data()` """
        self.team.get_context_data(team="Manchester_United", season="2019")
        mock_get_response.assert_called_with(
            url="https://understat.com/team/Manchester_United/2019",
            query="statisticsData",
        )


@patch.object(requests.Session, "get", side_effect=mocked_requests_get)
class TestTeamEndpointErrors(unittest.TestCase):
    """ Test error handling in `TeamEndpoint` """

    def setUp(self):
        """ setUp """
        self.player = TeamEndpoint(session=requests.Session())

    def test_get_data_bad_player(self, mock_get):
        """ test that `get_data()` raises an InvalidTeam error """
        with self.assertRaises(InvalidTeam):
            self.player.get_data(
                team="", season="", query="playersData", status_code=404
            )


class TestTeamEndpointDunder(unittest.TestCase):
    """ Tests for all `__*__()` methods of `TeamEndpoint()` """

    def setUp(self):
        """ setUp """
        self.team = TeamEndpoint(session=requests.Session())

    def test_repr(self):
        """ Test `__repr__()` """
        self.assertEqual(repr(self.team), "<TeamEndpoint>")


if __name__ == "__main__":
    unittest.main()
