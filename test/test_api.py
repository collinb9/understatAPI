""" Test APIClient """
import unittest
import tracemalloc
from unittest.mock import patch
import requests
from selenium.common.exceptions import WebDriverException
from understatapi import UnderstatClient
from understatapi.services import Search


class TestUnderstatClient(unittest.TestCase):
    """ Tests  `UnderstatClient"""

    def setUp(self):
        self.understat = UnderstatClient()

    def tearDown(self):
        self.understat.session.close()

    def test_league(self):
        """ test `league()` """
        self.assertEqual(
            repr(self.understat.league(league="")), "<LeagueEndpoint>"
        )

    def test_player(self):
        """ test `player()` """
        self.assertEqual(
            repr(self.understat.player(player="")), "<PlayerEndpoint>"
        )

    def test_team(self):
        """ test `team()` """
        self.assertEqual(repr(self.understat.team(team="")), "<TeamEndpoint>")

    def test_match(self):
        """ test `match()` """
        self.assertEqual(
            repr(self.understat.match(match="")), "<MatchEndpoint>"
        )

    @patch.object(Search, "get_player_ids")
    def test_search(self, mock_get_player_ids):
        """ test `search()` """
        player_ids = ["1", "2", "3"]
        mock_get_player_ids.side_effect = player_ids
        for player_id, return_value in zip(
            player_ids, self.understat.search("Ronaldo")
        ):
            with self.subTest(id=player_id):
                self.assertEqual(player_id, return_value.player)

    @patch.object(Search, "__init__")
    def test_search_web_driver_error(self, mock_get_player_ids):
        """
        test that `search()` raises a custom exception if `geckodriver`
        is not installed
        """
        mock_get_player_ids.side_effect = WebDriverException()
        with self.assertRaisesRegex(
            WebDriverException,
            "You must have 'geckodriver' installed to use "
            "UnderstatClient.search()",
        ):
            _ = list(self.understat.search(""))

    @patch.object(requests.Session, "close")
    def test_context_manager(self, mock_close):
        """
        Test that `UnderstatClient` can be used as a context manager
        """
        with UnderstatClient() as understat:
            with self.subTest(test="session_exists"):
                self.assertIsInstance(understat.session, requests.Session)
        with self.subTest(test="close"):
            mock_close.assert_called_once()


if __name__ == "__main__":
    tracemalloc.start()
    unittest.main()
