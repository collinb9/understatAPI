# pylint: disable=unused-argument
# pylint: disable=invalid-name
# pylint: disable=too-many-instance-attributes
# pylint: disable=undefined-loop-variable
"""Test understatapi"""
from typing import Dict
import unittest
from unittest.mock import patch
import json
from test import mocked_requests_get
from test.mock_selenium import MockWebDriver, MockWebDriverWait
import requests
from selenium.common.exceptions import WebDriverException
from understatapi import UnderstatClient
from understatapi.services import Search
from understatapi.endpoints import PlayerEndpoint
from understatapi.exceptions import (
    InvalidMatch,
    InvalidPlayer,
    InvalidTeam,
    InvalidLeague,
    InvalidSeason,
)


def read_json(path: str) -> Dict:
    """Read json data"""
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    return data


class EndpointBaseTestCase(unittest.TestCase):
    """Base class for all endpoint ``unittest.TestCase``` classes"""

    def setUp(self):
        self.understat = UnderstatClient()
        self.match_id = "dummy_match"
        self.match = self.understat.match(self.match_id)
        self.league_name = "EPL"
        self.league = self.understat.league(self.league_name)
        self.player_id = "dummy_player"
        self.player = self.understat.player(self.player_id)
        self.team_name = "dummy_team"
        self.team = self.understat.team(self.team_name)

    def tearDown(self):
        self.understat.session.close()


@patch.object(requests.Session, "get")
class TestEndpointsResponse(EndpointBaseTestCase):
    """Test that endpoints return the expected output"""

    def test_match_get_shot_data(self, mock_get):
        """ test ``match.get_shot_data()`` """
        mock_get.return_value = mocked_requests_get(
            "test/resources/match.html"
        )
        data = self.match.get_shot_data()
        data_path = "test/resources/data/match_shotsdata.json"
        expected_data = read_json(data_path)
        self.assertDictEqual(expected_data, data)

    def test_match_get_roster_data(self, mock_get):
        """ test ``match.get_roster_data()`` """
        mock_get.return_value = mocked_requests_get(
            "test/resources/match.html"
        )
        data = self.match.get_roster_data()
        data_path = "test/resources/data/match_rostersdata.json"
        expected_data = read_json(data_path)
        self.assertDictEqual(expected_data, data)

    def test_match_get_match_info(self, mock_get):
        """ test ``match.get_match_info()`` """
        mock_get.return_value = mocked_requests_get(
            "test/resources/match.html"
        )
        data = self.match.get_match_info()
        data_path = "test/resources/data/match_matchinfo.json"
        expected_data = read_json(data_path)
        self.assertDictEqual(expected_data, data)

    def test_player_get_match_data(self, mock_get):
        """ test ``player.get_match_data()`` """
        mock_get.return_value = mocked_requests_get(
            "test/resources/player.html"
        )
        data = self.player.get_match_data()
        data_path = "test/resources/data/player_matchesdata.json"
        expected_data = read_json(data_path)
        for i, (record, expected_record) in enumerate(
            zip(data, expected_data)
        ):
            with self.subTest(record=i):
                self.assertDictEqual(record, expected_record)

    def test_get_shot_data_return_value(self, mock_get):
        """ test ``player.get_shot_data()`` """
        mock_get.return_value = mocked_requests_get(
            "test/resources/player.html"
        )
        data = self.player.get_shot_data()
        data_path = "test/resources/data/player_shotsdata.json"
        expected_data = read_json(data_path)
        for i, (record, expected_record) in enumerate(
            zip(data, expected_data)
        ):
            with self.subTest(record=i):
                self.assertDictEqual(record, expected_record)

    def test_player_get_season_data(self, mock_get):
        """ test ``player.get_season_data()`` """
        mock_get.return_value = mocked_requests_get(
            "test/resources/player.html"
        )
        data = self.player.get_season_data()
        data_path = "test/resources/data/player_groupsdata.json"
        expected_data = read_json(data_path)
        self.assertDictEqual(data, expected_data)

    def test_team_get_player_data(self, mock_get):
        """ test ``team.get_match_data()`` """
        mock_get.return_value = mocked_requests_get("test/resources/team.html")
        data = self.team.get_player_data(season="2019")
        data_path = "test/resources/data/team_playersdata.json"
        expected_data = read_json(data_path)
        for i, (record, expected_record) in enumerate(
            zip(data, expected_data)
        ):
            with self.subTest(record=i):
                self.assertDictEqual(record, expected_record)

    def test_team_get_match_data(self, mock_get):
        """ test ``team.get_match_data()`` """
        mock_get.return_value = mocked_requests_get("test/resources/team.html")
        data = self.team.get_match_data(season="2019")
        data_path = "test/resources/data/team_datesdata.json"
        expected_data = read_json(data_path)
        for i, (record, expected_record) in enumerate(
            zip(data, expected_data)
        ):
            with self.subTest(record=i):
                self.assertDictEqual(record, expected_record)

    def test_team_get_context_data(self, mock_get):
        """ test ``team.get_context_data()`` """
        mock_get.return_value = mocked_requests_get("test/resources/team.html")
        data = self.team.get_context_data(season="2019")
        data_path = "test/resources/data/team_statisticsdata.json"
        expected_data = read_json(data_path)
        self.assertDictEqual(data, expected_data)

    def test_league_get_team_data(self, mock_get):
        """ test ``league.get_team_data()`` """
        mock_get.return_value = mocked_requests_get(
            "test/resources/league_epl.html"
        )
        data = self.league.get_team_data(season="2019")
        data_path = "test/resources/data/league_teamsdata.json"
        expected_data = read_json(data_path)
        self.assertDictEqual(data, expected_data)

    def test_league_get_match_data(self, mock_get):
        """ test ``league.get_match_data()`` """
        mock_get.return_value = mocked_requests_get(
            "test/resources/league_epl.html"
        )
        data = self.league.get_match_data(season="2019")
        data_path = "test/resources/data/league_datesdata.json"
        expected_data = read_json(data_path)
        for i, (record, expected_record) in enumerate(
            zip(data, expected_data)
        ):
            with self.subTest(record=i):
                self.assertDictEqual(record, expected_record)

    def test_league_get_player_data(self, mock_get):
        """ test ``league.get_player_data()`` """
        mock_get.return_value = mocked_requests_get(
            "test/resources/league_epl.html"
        )
        data = self.league.get_player_data(season="2019")
        data_path = "test/resources/data/league_playersdata.json"
        expected_data = read_json(data_path)
        for i, (record, expected_record) in enumerate(
            zip(data, expected_data)
        ):
            with self.subTest(record=i):
                self.assertDictEqual(record, expected_record)


@patch.object(requests.Session, "get", side_effect=mocked_requests_get)
class TestEndpointErrors(EndpointBaseTestCase):
    """Test the conditions under which exceptions are expected"""

    def test_match_get_data_bad_player(self, mock_get):
        """ test that ``match._get_data()`` raises an InvalidMatch error """
        with self.assertRaises(InvalidMatch):
            self.match.get_shot_data(status_code=404)

    def test_match_get_data_type_error(self, mock_get):
        """
        test that ``mathc.get_data()`` raises a TypeError
        when ``match`` is not a string
        """
        match = self.understat.match(match=None)
        with self.assertRaises(TypeError):
            _ = match.get_shot_data()

    def test_get_data_bad_player(self, mock_get):
        """ test that ``player._get_data()`` raises an InvalidPlayer error """
        with self.assertRaises(InvalidPlayer):
            self.player.get_shot_data(status_code=404)

    def test_player_get_data_type_error(self, mock_get):
        """
        test that ``player._get_data()`` raises a TypeError
        when ``player`` is not a string
        """
        player = self.understat.player(None)
        with self.assertRaises(TypeError):
            _ = player.get_shot_data()

    def test_team_get_data_bad_team(self, mock_get):
        """ test that ``team._get_data()`` raises an InvalidTeam error """
        team = self.understat.team(self.team_name)
        with self.assertRaises(InvalidTeam):
            _ = team.get_match_data(season="2019", status_code=404)

    def test_team_get_data_type_error(self, mock_get):
        """
        test that ``team._get_data()`` raises a TypeError
        when ``team`` is not a string
        """
        team = self.understat.team(None)
        with self.assertRaises(TypeError):
            _ = team.get_match_data(season="")

    def test_league_get_data_bad_team(self, mock_get):
        """ test that ``league._get_data()`` raises an InvalidLeague error """
        league = self.understat.league("dummy_team")
        with self.assertRaises(InvalidLeague):
            _ = league.get_match_data(season="2019", status_code=404)

    def test_league_get_data_type_error(self, mock_get):
        """
        test that ``league._get_data()`` raises a TypeError
        when ``league`` is not a string
        """
        league = self.understat.league(None)
        with self.assertRaises(TypeError):
            _ = league.get_match_data(season="2019")

    def test_invalid_season(self, mock_get):
        """
        Test that an error is raised when you try to get data for a
        season before 2014
        """
        with self.assertRaises(InvalidSeason):
            _ = self.league.get_match_data(season="2013")

    def test_error_handling_method(self, mock_get):
        # pylint: disable=no-member
        """
        test the error handling works as expected when a method is called
        that does not belong to the given endpoint
        """
        with self.assertRaises(AttributeError) as err:
            with UnderstatClient() as understat:
                understat.team("").get_bad_data()
            self.assertEqual(
                str(err),
                "'TeamEndpoint' object has no attribute 'get_bad_data'\n"
                "Its public methods are ['get_context_data', "
                "'get_match_data', get_player_data']",
            )

    @patch.object(Search, "__init__")
    def test_search_web_driver_error(self, mock_get_player_ids, mock_get):
        """
        test that ``search()`` raises a custom exception if ``geckodriver``
        is not installed
        """
        mock_get_player_ids.side_effect = WebDriverException()
        with self.assertRaisesRegex(
            WebDriverException,
            "You must have 'geckodriver' installed to use "
            "UnderstatClient.search()",
        ):
            _ = list(self.understat.search(""))


class TestEndpointDunder(EndpointBaseTestCase):
    """Tests for the dunder methods in the endpoint class"""

    def test_league(self):
        """ test ``league()`` """
        self.assertEqual(
            repr(self.understat.league(league="EPL")),
            "<LeagueEndpoint('EPL')>",
        )

    def test_player(self):
        """ test ``player()`` """
        self.assertEqual(
            repr(self.understat.player(player="1234")),
            "<PlayerEndpoint('1234')>",
        )

    def test_team(self):
        """ test ``team()`` """
        self.assertEqual(
            repr(self.understat.team(team="Manchester_United")),
            "<TeamEndpoint('Manchester_United')>",
        )

    def test_match(self):
        """ test ``match()`` """
        self.assertEqual(
            repr(self.understat.match(match="1234")), "<MatchEndpoint('1234')>"
        )

    def test_iteration(self):
        """Test iterating over players"""
        player_names = ["player_1", "player_2"]
        self.player._primary_attr = player_names
        for player, player_name in zip(self.player, player_names):
            with self.subTest(player=player_name):
                self.assertEqual(player.player, player_name)

    def test_len_one(self):
        """Test len() when there is only one player"""
        self.assertEqual(1, len(self.player))

    def test_len_error(self):
        """Test len() errors out when passed a non-sequence"""
        self.player._primary_attr = None
        with self.assertRaises(TypeError):
            self.assertEqual(1, len(self.player))

    def test_getitem_one(self):
        """Test getitem() when there is only one player"""
        self.assertEqual(self.player[0].player, self.player.player)

    def test_context_manager(self):
        """
        Test that the client behaves as a context manager as expected
        """
        try:
            with UnderstatClient():
                pass
        except Exception:  # pylint: disable=broad-except
            self.fail()


class TestSearch(unittest.TestCase):
    """ Test ``Search`` service """

    def setUp(self):
        """ setUp """
        self.url = "test/resources/home.html"
        self.real_url = Search.url
        Search.url = self.url
        self.real_web_driver = Search._web_driver
        Search._web_driver = MockWebDriver
        self.understat = UnderstatClient()

    def tearDown(self):
        self.understat.session.close()
        Search._web_driver = self.real_web_driver
        Search.url = self.real_url

    def test_search(self):
        """Test the search endpoint"""
        search = self.understat.search(player_name="Ronaldo")
        with patch(
            "understatapi.services.search.WebDriverWait", new=MockWebDriverWait
        ):
            for i, player in enumerate(search):
                # Looking at the exact output here is unhelpful because
                # of the limitations of mocking here. Need to perform
                # integration tests here
                with self.subTest(test="return value"):
                    self.assertIsInstance(player, PlayerEndpoint)
        with self.subTest(test="number of players returned"):
            self.assertEqual(i, 2)

    def test_search_with_max_ids(self):
        """
        Test the search endpoint where ``max_ids`` is less than the total
        number of results
        """
        search = self.understat.search(player_name="Ronaldo", max_ids=2)
        with patch(
            "understatapi.services.search.WebDriverWait", new=MockWebDriverWait
        ):
            for i, player in enumerate(search):
                # Looking at the exact output here is unhelpful because
                # of the limitations of mocking here. Need to perform
                # integration tests here
                with self.subTest(test="return value"):
                    self.assertIsInstance(player, PlayerEndpoint)
        with self.subTest(test="number of players returned"):
            self.assertEqual(i, 1)


if __name__ == "__main__":
    unittest.main()
