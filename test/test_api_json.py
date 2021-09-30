"""Test understatapi"""
from typing import Dict
import unittest
from unittest.mock import patch
import json
from test import mocked_requests_get
import requests
from understatapi import UnderstatClient
from understatapi.endpoints import BaseEndpoint


def save_data(data, path):
    """Save json data"""
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh)


def read_json(path: str) -> Dict:
    """Read json data"""
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    return data


class EndpointBaseTestCase(unittest.TestCase):
    """Base class for all endpoint ``unittest.TestCase``` classes"""

    def setUp(self):
        self.understat = UnderstatClient(return_dataframe=False)
        self.match_id = "dummy"
        self.match = self.understat.match(self.match_id)

    def tearDown(self):
        self.understat.session.close()


@patch.object(BaseEndpoint, "_request_url")
@patch.object(requests.Session, "get", side_effect=mocked_requests_get)
class TestEndpointsResponse(EndpointBaseTestCase):
    """Test that endpoints return the expected output"""

    def test_match_get_shot_data(self, mock_get, mock_request_url):
        """ test ``get_shot_data()`` """
        mock_request_url.return_value = mocked_requests_get(
            "test/resources/match.html"
        )
        data = self.match.get_shot_data()
        data_path = "test/resources/data/match_shotsdata.json"
        expected_data = read_json(data_path)
        self.assertDictEqual(expected_data, data)

    def test_match_get_roster_data(self, mock_get, mock_request_url):
        """ test ``get_roster_data()`` """
        mock_request_url.return_value = mocked_requests_get(
            "test/resources/match.html"
        )
        data = self.match.get_roster_data()
        data_path = "test/resources/data/match_rostersdata.json"
        expected_data = read_json(data_path)
        self.assertDictEqual(expected_data, data)

    def test_match_get_match_info(self, mock_get, mock_request_url):
        """ test ``get_match_info()`` """
        mock_request_url.return_value = mocked_requests_get(
            "test/resources/match.html"
        )
        data = self.match.get_match_info()
        data_path = "test/resources/data/match_matchinfo.json"
        # save_data(data, data_path)
        expected_data = read_json(data_path)
        self.assertDictEqual(expected_data, data)


@patch.object(BaseEndpoint, "_request_url")
@patch.object(requests.Session, "get", side_effect=mocked_requests_get)
@patch.object(BaseEndpoint, "_get_response")
class TestEndpointArguments(EndpointBaseTestCase):
    """Test that endpoints receive the expectred arguments"""

    def test_match_get_shot_data_args(
        self, mock_get_response, mock_get, mock_request_url
    ):
        """ test ``get_shot_data()`` """
        self.match.get_shot_data()
        mock_get_response.assert_called_with(
            url=f"https://understat.com/match/{self.match_id}",
            query="shotsData",
        )

    def test_get_roster_data_args(
        self, mock_get_response, mock_get, mock_request_url
    ):
        """ test ``get_roster_data()`` """
        self.match.get_roster_data()
        mock_get_response.assert_called_with(
            url=f"https://understat.com/match/{self.match_id}",
            query="rostersData",
        )

    def test_get_match_info_data_args(
        self, mock_get_response, mock_get, mock_request_url
    ):
        """ test ``get_match_info()`` """
        self.match.get_match_info()
        mock_get_response.assert_called_with(
            url=f"https://understat.com/match/{self.match_id}",
            query="match_info",
        )


if __name__ == "__main__":
    unittest.main()