# pylint: disable=unused-argument
# pylint: disable=duplicate-code
""" Test MatchEndpoint """
import unittest
from unittest.mock import patch
from test import mocked_requests_get, assert_data_equal
import requests
import pandas as pd
from understatapi.endpoints import MatchEndpoint, BaseEndpoint
from understatapi.exceptions import InvalidMatch


@patch.object(BaseEndpoint, "request_url")
@patch.object(requests.Session, "get", side_effect=mocked_requests_get)
class TestMatchEndpoint(unittest.TestCase):
    """ Tests for `MatchEndpoint` """

    def setUp(self):
        """ setUp """
        self.match = MatchEndpoint(session=requests.Session)
        self.base = BaseEndpoint(session=requests.Session)

    def test_get_shot_data_return_value(self, mock_get, mock_request_url):
        """ test `get_shot"_data()` """
        mock_request_url.return_value = mocked_requests_get(
            "test/resources/match.html"
        )
        data = self.match.get_shot_data(match="14717")
        data = self.base.unpack_dataframe(data)
        expected_data = pd.read_csv(
            "test/resources/data/match_shotsdata.csv", index_col=0
        )
        assert_data_equal(data, expected_data)

    @patch.object(BaseEndpoint, "get_response")
    def test_get_shot_data_args(
        self, mock_get_response, mock_get, mock_request_url
    ):
        """ test `get_shot_data()` """
        self.match.get_shot_data(match="14717")
        mock_get_response.assert_called_with(
            url="https://understat.com/match/14717",
            query="shotsData",
        )

    def test_get_roster_data_return_value(self, mock_get, mock_request_url):
        """ test `get_roster_data()` """
        mock_request_url.return_value = mocked_requests_get(
            "test/resources/match.html"
        )
        data = self.match.get_roster_data(match="14717")
        data = self.base.unpack_dataframe(data)
        expected_data = pd.read_csv(
            "test/resources/data/match_rostersdata.csv", index_col=0
        )
        assert_data_equal(data, expected_data)

    @patch.object(BaseEndpoint, "get_response")
    def test_get_roster_data_args(
        self, mock_get_response, mock_get, mock_request_url
    ):
        """ test `get_roster_data()` """
        self.match.get_roster_data(match="14717")
        mock_get_response.assert_called_with(
            url="https://understat.com/match/14717",
            query="rostersData",
        )

    def test_get_match_info_return_value(self, mock_get, mock_request_url):
        """ test `get_match_info()` """
        mock_request_url.return_value = mocked_requests_get(
            "test/resources/match.html"
        )
        data = self.match.get_match_info(match="14717")
        data = self.base.unpack_dataframe(data)
        expected_data = pd.read_csv(
            "test/resources/data/match_matchinfo.csv", index_col=0
        )
        assert_data_equal(data, expected_data)

    @patch.object(BaseEndpoint, "get_response")
    def test_get_match_info_data_args(
        self, mock_get_response, mock_get, mock_request_url
    ):
        """ test `get_match_info()` """
        self.match.get_match_info(match="14717")
        mock_get_response.assert_called_with(
            url="https://understat.com/match/14717",
            query="match_info",
        )


@patch.object(requests.Session, "get", side_effect=mocked_requests_get)
class TestMatchEndpointErrors(unittest.TestCase):
    """ Test error handling in `MatchEndpoint` """

    def setUp(self):
        """ setUp """
        self.match = MatchEndpoint(session=requests.Session())

    def test_get_data_bad_player(self, mock_get):
        """ test that `get_data()` raises an InvalidMatch error """
        with self.assertRaises(InvalidMatch):
            self.match.get_data(match="", query="shotsData", status_code=404)


class TestMatchEndpointDunder(unittest.TestCase):
    """ Tests for all `__*__()` methods of `MatchEndpoint()` """

    def setUp(self):
        """ setUp """
        self.team = MatchEndpoint(session=requests.Session())

    def test_repr(self):
        """ Test `__repr__()` """
        self.assertEqual(repr(self.team), "<MatchEndpoint>")


if __name__ == "__main__":
    unittest.main()
