""" Integration tests fo understatapi """
import os
import unittest
import tracemalloc
import requests
from understatapi.services import Search
from understatapi import UnderstatClient

try:
    RUN_TESTS = bool(os.environ["UNDERSTAT_INTEGRATION"])
except KeyError:
    RUN_TESTS = False


@unittest.skipIf(not RUN_TESTS, "UNDERSTAT_INTEGRATION not set to True")
class TestIntegrationSeleium(unittest.TestCase):
    """ Integration test for functions using selenium """

    def setUp(self):
        self.search = Search(player_name="Ronaldo", session=requests.Session())

    def tearDown(self):
        self.search.__exit__(None, None, None)
        self.search.session.close()

    def test_get_player_ids(self):
        """ test `get_player_ids()` """
        self.assertListEqual(
            list(self.search.get_player_ids()), ["2371", "2028", "7097"]
        )

    def test_search_invalid_player(self):
        """
        test what happens when `Search` is passed a search term which has
        no matches
        """
        self.search.player_name = "abcdef"
        self.assertListEqual(list(self.search.get_player_ids()), [])


@unittest.skipIf(not RUN_TESTS, "UNDERSTAT_INTEGRATION not set to True")
class TestIntegrationUnderstatClient(unittest.TestCase):
    """ Integration tests for interactions with `UnderstatClient` """

    def setUp(self):
        self.understat = UnderstatClient()

    def tearDown(self):
        self.understat.__exit__(None, None, None)

    def test_cookie_transfer(self):
        """
        Test that cookies get transferred from the selenium `WebDriver` object
        to the `requests.Session` object
        """
        with self.subTest(test="before"):
            self.assertEqual(len(self.understat.session.cookies), 0)
        list(self.understat.search("Cristiano Ronaldo"))
        with self.subTest(test="after"):
            self.assertEqual(len(self.understat.session.cookies), 7)


if __name__ == "__main__":
    tracemalloc.start()
    unittest.main()
