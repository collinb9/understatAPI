# pylint: disable=unused-argument
# pylint: disable=duplicate-code
""" Test BaseEndpoint """
import unittest
import tracemalloc
from unittest.mock import patch, mock_open
from test import mocked_requests_get, assert_data_equal
import requests
from requests.exceptions import HTTPError
import numpy as np
import pandas as pd
from understatapi.endpoints import BaseEndpoint
from understatapi.exceptions import InvalidQuery, InvalidLeague, InvalidSeason


class TestCheckArgs(unittest.TestCase):
    """ Tests for `_check_args()` """

    def setUp(self):
        self.base = BaseEndpoint("", session=requests.Session())

    def tearDown(self):
        self.base.session.close()

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


@patch.object(requests.Session, "get", side_effect=mocked_requests_get)
class TestBaseRequests(unittest.TestCase):
    """ Tests for `BaseEndpoint` methods that use requests module"""

    def setUp(self):
        self.base = BaseEndpoint("", session=requests.Session())

    def tearDown(self):
        self.base.session.close()

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
            query="teamsData",
        )
        data = self.base.unpack_dataframe(data)
        expected_data = pd.read_csv(
            "test/resources/league_epl_teamsdata.csv", index_col=0
        )
        assert_data_equal(data, expected_data)

    def test_get_response_datesdata(self, mock_get):
        """ Test `get_response()` works with `query='datesData'` """
        data = self.base.get_response(
            "test/resources/league_epl.html",
            query="datesData",
        )
        data = self.base.unpack_dataframe(data)
        expected_data = pd.read_csv(
            "test/resources/league_epl_datesdata.csv", index_col=0
        )
        assert_data_equal(data, expected_data)

    def test_get_response_playersdata(self, mock_get):
        """ Test `get_response()` works with `query='playersData'` """
        data = self.base.get_response(
            "test/resources/league_epl.html",
            query="playersData",
        )
        expected_data = pd.read_csv(
            "test/resources/league_epl_playersdata.csv", index_col=0
        )
        assert_data_equal(data, expected_data)


class TestExtractData(unittest.TestCase):
    """ Tests for `BaseEndpoint` methods involved in data extraction """

    def setUp(self):
        """ setUp """
        self.base = BaseEndpoint("", session=requests.Session())
        with open("test/resources/league_epl.html") as file:
            self.html = file.read()

    def tearDown(self):
        self.base.session.close()

    def test_extract_data_from_html_fails(self):
        """ test that ectract_data_from_html fails correctly """
        with self.assertRaisesRegex(
            InvalidQuery,
            "There is no html entry matching the query invalidQuery",
        ):
            self.base.extract_data_from_html(self.html, query="invalidQuery")

    def test_extract_data_from_html(self):
        """ Test extract_data_from_html """
        data = self.base.extract_data_from_html(self.html, query="teamsData")
        self.assertTupleEqual(data.shape, (20, 3))

    def test_json_to_dataframe_dict(self):
        """ test `json_to_dataframe()` when it is passed a dict """
        data = {"col1": [1, 2], "col2": [3, 4]}
        data = self.base.json_to_dataframe(data)
        expected_data = pd.DataFrame(
            data=[[1, 3], [2, 4]], columns=["col1", "col2"]
        )
        pd.testing.assert_frame_equal(data, expected_data)

    def test_json_to_dataframe_list_dict(self):
        """
        test `json_to_dataframe()` when it is passed a list of dictionaries
        """
        data = [{"col1": 1, "col2": 3}, {"col1": 2, "col2": 4}]
        data = self.base.json_to_dataframe(data)
        expected_data = pd.DataFrame(
            data=[[1, 3], [2, 4]], columns=["col1", "col2"]
        )
        pd.testing.assert_frame_equal(data, expected_data)

    def test_unpack_dataframe(self):
        """ test `unpack_dataframe()` """
        data = pd.DataFrame()
        data["side"] = ["h", "a"]
        data["goals"] = [{"h": 1, "a": 0}, {"h": 5, "a": 5}]
        data = self.base.unpack_dataframe(data)
        expected_data = pd.DataFrame(
            data=[["h", 1, 0], ["a", 5, 5]],
            columns=["side", "goals_h", "goals_a"],
        )
        pd.testing.assert_frame_equal(data, expected_data)

    def test_try_json_normalize_use(self):
        """ test `try_json_normalize()` with a `pd.Series` of dictionaries"""
        data = pd.Series(
            [{"h": 1, "a": 0}, {"h": 5, "a": 5}, np.nan], name="goals"
        )
        data = self.base.try_json_normalize(data)
        expected_data = pd.DataFrame(
            data=[[1, 0], [5, 5], [np.nan, np.nan]],
            columns=["goals_h", "goals_a"],
        )
        pd.testing.assert_frame_equal(data, expected_data)

    def test_try_json_normalize_pass(self):
        """ test `try_json_normalize()` with a `pd.Series` of integers"""
        data = pd.Series([1, 2], name="goals")
        data = self.base.try_json_normalize(data)
        expected_data = pd.DataFrame(
            data=[1, 2],
            columns=["goals"],
        )
        pd.testing.assert_frame_equal(data, expected_data)


class TestBaseEndpointDunder(unittest.TestCase):
    """ Tests for all `__*__()` methods of `BaseEndpoint()` """

    def setUp(self):
        """ setUp """
        self.base = BaseEndpoint(None, session=requests.Session())

    def tearDown(self):
        self.base.session.close()

    def test_repr(self):
        """ Test `__repr__()` """
        self.assertEqual(repr(self.base), "<BaseEndpoint>")

    def test_init(self):
        """ Test `__init__()` """
        with self.subTest(test="session"):
            self.assertIsInstance(self.base.session, requests.Session)
        with self.subTest(test="_primary_attr"):
            self.assertIsNone(self.base._primary_attr)

    def test_len(self):
        """ Test `__len__()` """
        with self.subTest(test="None"):
            with self.assertRaises(TypeError):
                len(self.base)
        self.base._primary_attr = "123"
        with self.subTest(test="str"):
            self.assertEqual(len(self.base), 1)
        self.base._primary_attr = ["1", "2"]
        with self.subTest(test="list"):
            self.assertEqual(len(self.base), 2)

    def test_getitem(self):
        """ Test `__getitem__()` """
        with self.subTest(test="None"):
            with self.assertRaises(TypeError):
                _ = self.base[0]
        self.base._primary_attr = "123"
        with self.subTest(test="str"):
            self.assertEqual("123", self.base[0]._primary_attr)
        list_attr = ["1", "2"]
        self.base._primary_attr = list_attr
        for i, item in enumerate(list_attr):
            with self.subTest(test=f"list_{item}"):
                self.assertEqual(self.base[i]._primary_attr, list_attr[i])
        with self.subTest(test="index_error"):
            with self.assertRaises(IndexError):
                _ = self.base[2]


if __name__ == "__main__":
    tracemalloc.start()
    unittest.main()
