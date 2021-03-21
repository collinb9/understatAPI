""" Test APIClient """
import unittest
from unittest.mock import patch
import requests
from understatapi import UnderstatClient


class TestAPIClientDunder(unittest.TestCase):
    """ Tests for all `__*__()` methods of `BaseEndpoint()` """

    def setUp(self):
        """ setUp() """
        self.understat = UnderstatClient()

    def test_init(self):
        """ test `__init__()` """
        with self.subTest(test="league_endpoint"):
            self.assertEqual(repr(self.understat.league), "<LeagueEndpoint>")
        with self.subTest(test="player_endpoint"):
            self.assertEqual(repr(self.understat.player), "<PlayerEndpoint>")
        with self.subTest(test="team_endpoint"):
            self.assertEqual(repr(self.understat.team), "<TeamEndpoint>")
        with self.subTest(test="match_endpoint"):
            self.assertEqual(repr(self.understat.match), "<MatchEndpoint>")

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
