# pylint: disable=unused-argument
""" Test BaseEndpoint """
import unittest
from ast import literal_eval
from unittest.mock import patch, mock_open
from test import mocked_requests_get
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
import pandas as pd
from understatapi.endpoints import BaseEndpoint
from understatapi.exceptions import InvalidQuery, InvalidLeague, InvalidSeason


class TestCheckArgs(unittest.TestCase):
    """ Tests for `_check_args()` """

    def setUp(self):
        """ setUp """
        self.base = BaseEndpoint()

    def test_invalid_season(self):
        """ test that `_check_args()` raises InvalidSeason """
        with self.assertRaises(InvalidSeason):
            self.base._check_args(season="2013")

    def test_invalid_league(self):
        """ test that `_check_args()` raises InvalidLeague """
        with self.assertRaises(InvalidLeague):
            self.base._check_args(league="not_a_league")

    def test_invalid_query(self):
        """ test that `_check_args()` raises InvalidQuery """
        with self.assertRaises(InvalidQuery):
            self.base._check_args(query="datesData")


@patch("requests.get", side_effect=mocked_requests_get)
class TestBaseRequests(unittest.TestCase):
    """ Tests for `BaseEndpoint` methods that use requests module"""

    def setUp(self):
        """ setUp """
        self.base = BaseEndpoint()

    @patch("test.open", new_callable=mock_open)
    def test_get_response_fails(self, mock_get, mock_open_method):
        """ Test that get_response fails correctly """
        with self.assertRaises(HTTPError):
            self.base.request_url("https://understat.com/", status_code=404)

    @patch("test.open", new_callable=mock_open)
    def test_request_url(self, mock_get, mock_open_method):
        """ Test get_response """
        res = self.base.request_url(self.base.base_url)
        mock_open_method.assert_called_with("https://understat.com/")
        self.assertEqual(res.url, "https://understat.com/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.reason, "OK")

    def test_get_response_teamsdata(self, mock_get):
        """ Test `get_response()` works with `query='teamsData'` """
        data = self.base.get_response(
            "test/resources/league_epl.html",
            element="script",
            query="teamsData",
        )
        expected_data = pd.read_csv(
            "test/resources/league_epl_teamsdata.csv", index_col=0
        )
        expected_data.index = expected_data.index.astype(str)
        expected_data.id = expected_data.id.astype(str)
        expected_data.history = expected_data.history.apply(literal_eval)
        pd.testing.assert_frame_equal(data, expected_data, check_dtype=False)

    def test_get_response_datesdata(self, mock_get):
        """ Test `get_response()` works with `query='datesData'` """
        data = self.base.get_response(
            "test/resources/league_epl.html",
            element="script",
            query="datesData",
        )
        expected_data = pd.read_csv(
            "test/resources/league_epl_datesdata.csv", index_col=0
        )
        expected_data.id = expected_data.id.astype(str)
        expected_data.h = expected_data.h.apply(literal_eval)
        expected_data.a = expected_data.a.apply(literal_eval)
        expected_data.goals = expected_data.goals.apply(literal_eval)
        expected_data.xG = expected_data.xG.apply(literal_eval)
        expected_data.forecast.loc[
            ~expected_data.forecast.isna()
        ] = expected_data.forecast.loc[~expected_data.forecast.isna()].apply(
            literal_eval
        )
        pd.testing.assert_frame_equal(data, expected_data, check_dtype=False)

    def test_get_response_playersdata(self, mock_get):
        """ Test `get_response()` works with `query='playersData'` """
        data = self.base.get_response(
            "test/resources/league_epl.html",
            element="script",
            query="playersData",
        )
        expected_data = pd.read_csv(
            "test/resources/league_epl_playersdata.csv", index_col=0
        )
        data.xG = data.xG.astype(float)
        data.xA = data.xA.astype(float)
        expected_data.loc[
            :, ~expected_data.columns.str.contains("xG|xA")
        ] = expected_data.loc[
            :, ~expected_data.columns.str.contains("xG|xA")
        ].astype(
            str
        )
        data.loc[:, data.columns.str.contains("xG|xA")] = data.loc[
            :, data.columns.str.contains("xG|xA")
        ].astype(float)
        pd.testing.assert_frame_equal(data, expected_data, check_dtype=False)


class TestExtractData(unittest.TestCase):
    """ Tests for `BaseEndpoint` methods involved in data extraction """

    def setUp(self):
        """ setUp """
        self.base = BaseEndpoint()
        with open("test/resources/league_epl.html") as file:
            self.soup = BeautifulSoup(file, "lxml")

    def test_extract_data_from_html_fails(self):
        """ test that ectract_data_from_html fails correctly """
        with self.assertRaisesRegex(
            InvalidQuery,
            "There is no html entry matching the query invalidQuery",
        ):
            self.base.extract_data_from_html(
                self.soup, element="", query="invalidQuery"
            )

    def test_extract_data_from_html(self):
        """ Test extract_data_from_html """
        data = self.base.extract_data_from_html(
            self.soup, element="script", query="teamsData"
        )
        self.assertTupleEqual(data.shape, (20, 3))


class TestBaseEndpointDunder(unittest.TestCase):
    """ Tests for all `__*__()` methods of `BaseEndpoint()` """

    def setUp(self):
        """ setUp """
        self.base = BaseEndpoint()

    def test_repr(self):
        """ Test `__repr__()` """
        self.assertEqual(repr(self.base), "<BaseEndpoint>")


if __name__ == "__main__":
    unittest.main()
