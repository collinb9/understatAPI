""" Test APIClient """
import unittest
from understatapi import APIClient


class TestAPIClientDunder(unittest.TestCase):
    """ Tests for all `__*__()` methods of `BaseEndpoint()` """

    def setUp(self):
        """ setUp() """
        self.understat = APIClient()

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
