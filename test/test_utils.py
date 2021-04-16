# pylint: disable=no-self-use
""" Tests for ``understatapi.utils`` """
import unittest
import pandas as pd
import numpy as np
import understatapi.utils as utils
from understatapi.endpoints import BaseEndpoint


class Spam:
    """ Dummy class """

    def __init__(self):
        self._attr = None

    @property
    def attr(self):
        """ attr """
        return self._attr

    @attr.setter
    def attr(self, _attr):
        self._attr = _attr

    @classmethod
    def with_attr(cls, attr):
        """ with attribute """
        instance = cls()
        instance.attr = attr
        return instance

    def _ham(self):
        """ ham """

    def eggs(self):
        """ spam """


class TestUtils(unittest.TestCase):
    """ Test functions in ``understatapi.utils`` """

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

    def test_get_all_methods(self):
        """ test ``get_all_methods`` """
        self.assertListEqual(
            utils.get_all_methods(Spam), ["__init__", "_ham", "eggs"]
        )

    def test_get_public_methods(self):
        """ test ``get_public_methods`` """
        self.assertListEqual(utils.get_public_methods(Spam), ["eggs"])

    def test_find_endpoints(self):
        """ test ``find_endpoint`` """
        text = """nothing here
        there is a 'BaseEndpoint' here
        this Endpoint should not be found
        TeamEndpoint OtherEndpoint - 2 endpoints
        """
        for i, line in enumerate(text.split("\n")):
            with self.subTest(line=i):
                match = utils.find_endpoints(line)
                if i in [0, 2]:
                    self.assertIsNone(match)
                elif i == 1:
                    self.assertListEqual(match, ["BaseEndpoint"])
                elif i == 3:
                    self.assertListEqual(
                        match, ["TeamEndpoint", "OtherEndpoint"]
                    )

    def test_str_to_class(self):
        """ test ``str_to_class`` """
        self.assertIs(
            utils.str_to_class(__name__, "BaseEndpoint"), BaseEndpoint
        )


if __name__ == "__main__":
    unittest.main()
