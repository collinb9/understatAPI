"""Test understatapi"""
import unittest
from unittest.mock import patch
import json
from test import mocked_requests_get
import requests
from understatapi import UnderstatClient
from understatapi.endpoints import BaseEndpoint


def save_data(data, path):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh)


@patch.object(BaseEndpoint, "_request_url")
@patch.object(requests.Session, "get", side_effect=mocked_requests_get)
class TestMatch(unittest.TestCase):
    """ Test MatchEndpoint """

    def setUp(self):
        self.understat = UnderstatClient(return_dataframe=False)

    def tearDown(self):
        self.understat.session.close()

    def test_match_get_shot_data(self, mock_get, mock_request_url):
        mock_request_url.return_value = mocked_requests_get(
            "test/resources/match.html"
        )
        match = self.understat.match(match="dummy")
        data = match.get_shot_data()
        data_path = "test/resources/data/match_shotsdata.csv"
        print(data)


if __name__ == "__main__":
    unittest.main()