# pylint: disable=unused-argument
# pylint: disable=duplicate-code
""" Test PlayerEndpoint """
import unittest
from unittest.mock import patch
from test import mocked_requests_get, assert_data_equal
import requests
import pandas as pd
from understatapi.endpoints import PlayerEndpoint, BaseEndpoint
from understatapi.exceptions import InvalidPlayer


@patch.object(BaseEndpoint, "request_url")
@patch.object(requests.Session, "get", side_effect=mocked_requests_get)
class TestPlayerEndpoint(unittest.TestCase):
    """ Tests for `PlayerEndpoint` """

    def setUp(self):
        """ setUp """
        self.player = PlayerEndpoint(session=requests.Session())
        self.base = BaseEndpoint(session=requests.Session())

    def test_get_match_data_return_value(self, mock_get, mock_request_url):
        """ test `get_match_data()` """
        mock_request_url.return_value = mocked_requests_get(
            "test/resources/player.html"
        )
        data = self.player.get_match_data(player="647")
        expected_data = pd.read_csv(
            "test/resources/data/player_matchesdata.csv", index_col=0
        )
        assert_data_equal(data, expected_data)

    @patch.object(BaseEndpoint, "get_response")
    def test_get_match_data_args(
        self, mock_get_response, mock_get, mock_request_url
    ):
        """ test `get_match_data()` """
        self.player.get_match_data(player="647")
        mock_get_response.assert_called_with(
            url="https://understat.com/player/647",
            query="matchesData",
        )

    def test_get_shot_data_return_value(self, mock_get, mock_request_url):
        """ test `get_shot_data()` """
        mock_request_url.return_value = mocked_requests_get(
            "test/resources/player.html"
        )
        data = self.player.get_shot_data(player="647")
        expected_data = pd.read_csv(
            "test/resources/data/player_shotsdata.csv", index_col=0
        )
        assert_data_equal(data, expected_data)

    @patch.object(BaseEndpoint, "get_response")
    def test_get_shot_data_args(
        self, mock_get_response, mock_get, mock_request_url
    ):
        """ test `get_shot_data()` """
        self.player.get_shot_data(player="647")
        mock_get_response.assert_called_with(
            url="https://understat.com/player/647",
            query="shotsData",
        )

    def test_get_season_data_return_value(self, mock_get, mock_request_url):
        """ test `get_season_data()` """
        mock_request_url.return_value = mocked_requests_get(
            "test/resources/player.html"
        )
        data = self.player.get_season_data(player="647")
        data = self.base.unpack_dataframe(data)
        expected_data = pd.read_csv(
            "test/resources/data/player_groupsdata.csv", index_col=0
        )
        assert_data_equal(data, expected_data)

    @patch.object(BaseEndpoint, "get_response")
    def test_get_season_data_args(
        self, mock_get_response, mock_get, mock_request_url
    ):
        """ test `get_season_data()` """
        self.player.get_season_data(player="647")
        mock_get_response.assert_called_with(
            url="https://understat.com/player/647",
            query="groupsData",
        )


@patch.object(requests.Session, "get", side_effect=mocked_requests_get)
class TestPlayerEndpointErrors(unittest.TestCase):
    """ Test error handling in `PlayerEndpoint` """

    def setUp(self):
        """ setUp """
        self.player = PlayerEndpoint(session=requests.Session())

    def test_get_data_bad_player(self, mock_get):
        """ test that `get_data()` raises an InvalidPlayer error """
        with self.assertRaises(InvalidPlayer):
            self.player.get_data(
                player="", query="matchesData", status_code=404
            )


class TestPlayerEndpointDunder(unittest.TestCase):
    """ Tests for all `__*__()` methods of `PlayerEndpoint()` """

    def setUp(self):
        """ setUp """
        self.player = PlayerEndpoint(session=requests.Session())

    def test_repr(self):
        """ Test `__repr__()` """
        self.assertEqual(repr(self.player), "<PlayerEndpoint>")
