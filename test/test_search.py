# pylint: disable=arguments-differ
# pylint: disable=unused-argument
""" Test Search service """
import time
import tracemalloc
import unittest
from unittest.mock import PropertyMock, patch, call
from test.mock_selenium import MockWebDriver, MockWebDriverWait
import requests
from selenium.webdriver.firefox.options import Options
from understatapi.services import Search


def make_url_with_player_id(player_id):
    """ Return the understat url for a given player id """
    return f"https://understat.com/player/{player_id}"


class TestSearch(unittest.TestCase):
    """ Test `Search` service """

    @patch(
        "understatapi.services.search.Search._initialise_browser",
    )
    def setUp(self, mock__initialise_browser):
        """ setUp """
        self.search = Search(player_name="Ronaldo", session=requests.Session())
        self.search.browser = MockWebDriver()

    def tearDown(self):
        self.search.__exit__(None, None, None)
        self.search.session.close()

    def test_init(self):
        """ test `__init__()` """
        with self.subTest(test="player_name"):
            self.search.player_name = "Ronaldo"
        with self.subTest(test="session"):
            self.assertIsInstance(self.search.session, requests.Session)
        with self.subTest(test="browser"):
            self.assertIsInstance(self.search.browser, MockWebDriver)
        with self.subTest(test="max_ids"):
            self.assertEqual(self.search.max_ids, 5)
        with self.subTest(test="page_load_timeout"):
            self.assertEqual(self.search.page_load_timeout, 5)

    def test_repr(self):
        """ test `__repr__()` """
        self.assertEqual(repr(self.search), "<Search>")

    def test_get_search_results(self):
        """ test `_get_search_results()` """
        self.search.browser.get("test/resources/home.html")
        players = self.search._get_search_results()
        expected_players = [
            ("Cristiano Ronaldo", "Juventus"),
            ("Ronaldo", "Empoli"),
            ("Ronaldo Vieira", "Verona"),
        ]
        self.assertListEqual(list(players), expected_players)

    @patch("understatapi.services.search.Search._wait_for_page_load")
    @patch.object(time, "sleep")
    def test_make_search(self, mock_sleep, mock_wait_for_page_load):
        """ test `_make_search()` """
        self.search.browser.get("test/resources/home.html")
        with patch(
            "understatapi.services.search.WebDriverWait", new=MockWebDriverWait
        ):
            self.search._make_search(wait_time=0.01)
            mock_sleep.assert_called_with(0.01)

    @patch.object(time, "sleep")
    def test_wait_for_page_load(self, mock_sleep):
        """ test _wait_for_page_load """
        with patch(
            "understatapi.services.search.WebDriverWait", new=MockWebDriverWait
        ):
            with self.subTest(timeout="False"):
                self.search._wait_for_page_load(wait_time=0.01)
                mock_sleep.assert_called_with(0.01)
            with self.subTest(timeout="True"):
                with self.assertRaises(TimeoutError):
                    self.search._wait_for_page_load(wait_time=100)

    @patch.object(Search, "_make_search")
    def test_cycle_results(self, mock_make_search):
        """ test `_cycle_results()` """
        expected_player_ids = ["2371", "2028", "7097"]
        with patch.object(
            MockWebDriver,
            "current_url",
            new=PropertyMock(
                side_effect=[
                    make_url_with_player_id(player_id)
                    for player_id in expected_player_ids
                ]
            ),
        ):
            self.search.browser.get("test/resources/home.html")
            results = [
                ("Cristiano Ronaldo", "Juventus"),
                ("Ronaldo", "Empoli"),
                ("Ronaldo Vieira", "Verona"),
            ]
            player_ids = list(self.search._cycle_results(results))
            self.assertListEqual(expected_player_ids, player_ids)
            mock_make_search.assert_has_calls([call()] * 3)

    def test_get_player_id_from_url(self):
        """ test `get_player_id_from_url()` """
        self.assertEqual(
            self.search._get_player_id_from_url(
                "https://understat.com/player/2371"
            ),
            "2371",
        )

    @patch.object(time, "sleep")
    def test_get_player_ids(self, mock_sleep):
        """ test `get_player_ids()` """
        self.search.url = "test/resources/home.html"
        expected_player_ids = ["2371", "2028", "7097"]
        with patch.object(
            MockWebDriver,
            "current_url",
            new=PropertyMock(
                side_effect=[
                    make_url_with_player_id(player_id)
                    for player_id in expected_player_ids
                ]
            ),
        ):
            with patch(
                "understatapi.services.search.WebDriverWait",
                new=MockWebDriverWait,
            ):
                player_ids = list(self.search.get_player_ids())
        self.assertListEqual(player_ids, expected_player_ids)

    @patch.object(time, "sleep")
    def test_get_player_ids_max_ids(self, mock_sleep):
        """ test `get_player_ids()` with `max_ids=1` """
        self.search.url = "test/resources/home.html"
        player_id_list = ["2371", "2028", "7097"]
        self.search.max_ids = 1
        with patch.object(
            MockWebDriver,
            "current_url",
            new=PropertyMock(
                side_effect=[
                    make_url_with_player_id(player_id)
                    for player_id in player_id_list
                ]
            ),
        ):
            with patch(
                "understatapi.services.search.WebDriverWait",
                new=MockWebDriverWait,
            ):
                player_ids = list(self.search.get_player_ids())
        expected_player_ids = ["2371"]
        self.assertListEqual(player_ids, expected_player_ids)

    @patch("understatapi.services.search.Firefox", autospec=True)
    def test_initialise_browser(self, mock_firefox):
        """ test `_initialise_browser()` """
        self.search._initialise_browser()
        mock_firefox.assert_called_once()
        _, kwargs = mock_firefox.call_args
        self.assertIsInstance(kwargs["options"], Options)

    @patch.object(MockWebDriver, "quit")
    @patch(
        "understatapi.services.search.Search._initialise_browser",
    )
    def test_context_manager(self, mock_initialise_browser, mock_quit):
        """ Test that `Search` works as a context manager """
        with Search(
            player_name="Ronaldo", session=requests.Session()
        ) as search:
            search.browser = MockWebDriver()
        with self.subTest(test="quit"):
            mock_quit.assert_called_once()
        with self.subTest(test="cookies"):
            self.assertListEqual(
                list(search.session.cookies.iteritems()),
                [("PHPSESSID", "00000"), ("UID", "11111")],
            )


if __name__ == "__main__":
    tracemalloc.start()
    unittest.main()
