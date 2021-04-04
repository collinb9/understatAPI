# pylint: disable=no-self-use
""" Tests for ``understatapi.utils`` """
import unittest
import pandas as pd
import numpy as np
import understatapi.utils as utils


class TestUtils(unittest.TestCase):
    """ Test functions in ``understatapi.utils`` """

    def setUp(self):
        """ setUp """

    def test_json_to_dataframe_dict(self):
        """ test ``json_to_dataframe()`` when it is passed a dict """
        data = {"col1": [1, 2], "col2": [3, 4]}
        data = utils.json_to_dataframe(data)
        expected_data = pd.DataFrame(
            data=[[1, 3], [2, 4]], columns=["col1", "col2"]
        )
        pd.testing.assert_frame_equal(data, expected_data)

    def test_json_to_dataframe_list_dict(self):
        """
        test ``json_to_dataframe()`` when it is passed a list of dictionaries
        """
        data = [{"col1": 1, "col2": 3}, {"col1": 2, "col2": 4}]
        data = utils.json_to_dataframe(data)
        expected_data = pd.DataFrame(
            data=[[1, 3], [2, 4]], columns=["col1", "col2"]
        )
        pd.testing.assert_frame_equal(data, expected_data)

    def test_unpack_dataframe(self):
        """ test ``unpack_dataframe()`` """
        data = pd.DataFrame()
        data["side"] = ["h", "a"]
        data["goals"] = [{"h": 1, "a": 0}, {"h": 5, "a": 5}]
        data = utils.unpack_dataframe(data)
        expected_data = pd.DataFrame(
            data=[["h", 1, 0], ["a", 5, 5]],
            columns=["side", "goals_h", "goals_a"],
        )
        pd.testing.assert_frame_equal(data, expected_data)

    def test_try_json_normalize_use(self):
        """
        test ``try_json_normalize()`` with a ``pd.Series``
        of dictionaries
        """
        data = pd.Series(
            [{"h": 1, "a": 0}, {"h": 5, "a": 5}, np.nan], name="goals"
        )
        data = utils.try_json_normalize(data)
        expected_data = pd.DataFrame(
            data=[[1, 0], [5, 5], [np.nan, np.nan]],
            columns=["goals_h", "goals_a"],
        )
        pd.testing.assert_frame_equal(data, expected_data)

    def test_try_json_normalize_pass(self):
        """ test ``try_json_normalize()`` with a ``pd.Series`` of integers"""
        data = pd.Series([1, 2], name="goals")
        data = utils.try_json_normalize(data)
        expected_data = pd.DataFrame(
            data=[1, 2],
            columns=["goals"],
        )
        pd.testing.assert_frame_equal(data, expected_data)


if __name__ == "__main__":
    unittest.main()
