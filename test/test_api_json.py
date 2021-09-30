"""Test understatapi"""
from typing import Dict
import unittest
from unittest.mock import patch
import json
from test import mocked_requests_get
import requests
from understatapi import UnderstatClient
from understatapi.endpoints import BaseEndpoint
from understatapi.exceptions import (
    InvalidMatch,
    InvalidPlayer,
    InvalidTeam,
    InvalidLeague,
)


def save_data(data, path):
    """Save json data"""
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh)


def read_json(path: str) -> Dict:
    """Read json data"""
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    return data


class EndpointBaseTestCase(unittest.TestCase):
    """Base class for all endpoint ``unittest.TestCase``` classes"""

    def setUp(self):
        self.understat = UnderstatClient(return_dataframe=False)
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


@patch.object(BaseEndpoint, "_request_url")
@patch.object(requests.Session, "get", side_effect=mocked_requests_get)
class TestEndpointsResponse(EndpointBaseTestCase):
    """Test that endpoints return the expected output"""

    def test_match_get_shot_data(self, mock_get, mock_request_url):
        """ test ``match.get_shot_data()`` """
        mock_request_url.return_value = mocked_requests_get(
            "test/resources/match.html"
        )
        data = self.match.get_shot_data()
        data_path = "test/resources/data/match_shotsdata.json"
        expected_data = read_json(data_path)
        self.assertDictEqual(expected_data, data)

    def test_match_get_roster_data(self, mock_get, mock_request_url):
        """ test ``match.get_roster_data()`` """
        mock_request_url.return_value = mocked_requests_get(
            "test/resources/match.html"
        )
        data = self.match.get_roster_data()
        data_path = "test/resources/data/match_rostersdata.json"
        expected_data = read_json(data_path)
        self.assertDictEqual(expected_data, data)

    def test_match_get_match_info(self, mock_get, mock_request_url):
        """ test ``match.get_match_info()`` """
        mock_request_url.return_value = mocked_requests_get(
            "test/resources/match.html"
        )
        data = self.match.get_match_info()
        data_path = "test/resources/data/match_matchinfo.json"
        expected_data = read_json(data_path)
        self.assertDictEqual(expected_data, data)

    def test_player_get_match_data(self, mock_get, mock_request_url):
        """ test ``player.get_match_data()`` """
        mock_request_url.return_value = mocked_requests_get(
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

    def test_get_shot_data_return_value(self, mock_get, mock_request_url):
        """ test ``player.get_shot_data()`` """
        mock_request_url.return_value = mocked_requests_get(
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

    def test_player_get_season_data(self, mock_get, mock_request_url):
        """ test ``player.get_season_data()`` """
        mock_request_url.return_value = mocked_requests_get(
            "test/resources/player.html"
        )
        data = self.player.get_season_data()
        data_path = "test/resources/data/player_groupsdata.json"
        expected_data = read_json(data_path)
        self.assertDictEqual(data, expected_data)

    def test_team_get_player_data(self, mock_get, mock__request_url):
        """ test ``team.get_match_data()`` """
        mock__request_url.return_value = mocked_requests_get(
            "test/resources/team.html"
        )
        data = self.team.get_player_data(season="2019")
        data_path = "test/resources/data/team_playersdata.json"
        expected_data = read_json(data_path)
        for i, (record, expected_record) in enumerate(
            zip(data, expected_data)
        ):
            with self.subTest(record=i):
                self.assertDictEqual(record, expected_record)

    def test_team_get_match_data(self, mock_get, mock__request_url):
        """ test ``team.get_match_data()`` """
        mock__request_url.return_value = mocked_requests_get(
            "test/resources/team.html"
        )
        data = self.team.get_match_data(season="2019")
        data_path = "test/resources/data/team_datesdata.json"
        expected_data = read_json(data_path)
        for i, (record, expected_record) in enumerate(
            zip(data, expected_data)
        ):
            with self.subTest(record=i):
                self.assertDictEqual(record, expected_record)

    def test_team_get_context_data(self, mock_get, mock__request_url):
        """ test ``team.get_context_data()`` """
        mock__request_url.return_value = mocked_requests_get(
            "test/resources/team.html"
        )
        data = self.team.get_context_data(season="2019")
        data_path = "test/resources/data/team_statisticsdata.json"
        # save_data(data, data_path)
        expected_data = read_json(data_path)
        self.assertDictEqual(data, expected_data)

    def test_league_get_team_data(self, mock_get, mock__request_url):
        """ test ``league.get_team_data()`` """
        mock__request_url.return_value = mocked_requests_get(
            "test/resources/league_epl.html"
        )
        data = self.league.get_team_data(season="2019")
        data_path = "test/resources/data/league_teamsdata.json"
        expected_data = read_json(data_path)
        self.assertDictEqual(data, expected_data)

    def test_league_get_match_data(self, mock_get, mock__request_url):
        """ test ``league.get_match_data()`` """
        mock__request_url.return_value = mocked_requests_get(
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

    def test_league_get_player_data(self, mock_get, mock__request_url):
        """ test ``league.get_player_data()`` """
        mock__request_url.return_value = mocked_requests_get(
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


@patch.object(BaseEndpoint, "_request_url")
@patch.object(requests.Session, "get", side_effect=mocked_requests_get)
@patch.object(BaseEndpoint, "_get_response")
class TestEndpointArguments(EndpointBaseTestCase):
    """Test that endpoints receive the expectred arguments"""

    def test_match_get_shot_data_args(
        self, mock_get_response, mock_get, mock_request_url
    ):
        """ test ``match.get_shot_data()`` """
        self.match.get_shot_data()
        mock_get_response.assert_called_with(
            url=f"https://understat.com/match/{self.match_id}",
            query="shotsData",
        )

    def test_match_get_roster(
        self, mock_get_response, mock_get, mock_request_url
    ):
        """ test ``match.get_roster_data()`` """
        self.match.get_roster_data()
        mock_get_response.assert_called_with(
            url=f"https://understat.com/match/{self.match_id}",
            query="rostersData",
        )

    def test_match_get_match_info(
        self, mock_get_response, mock_get, mock_request_url
    ):
        """ test ``match.get_match_info()`` """
        self.match.get_match_info()
        mock_get_response.assert_called_with(
            url=f"https://understat.com/match/{self.match_id}",
            query="match_info",
        )

    def test_player_get_match_data(
        self, mock_get_response, mock_get, mock_request_url
    ):
        """ test ``player.get_match_data()`` """
        self.player.get_match_data()
        mock_get_response.assert_called_with(
            url=f"https://understat.com/player/{self.player_id}",
            query="matchesData",
        )

    def test_player_get_shot_data(
        self, mock_get_response, mock_get, mock_request_url
    ):
        """ test ``player.get_shot_data()`` """
        self.player.get_shot_data()
        mock_get_response.assert_called_with(
            url=f"https://understat.com/player/{self.player_id}",
            query="shotsData",
        )

    def test_player_get_season_data(
        self, mock_get_response, mock_get, mock_request_url
    ):
        """ test ``player.get_season_data()`` """
        self.player.get_season_data()
        mock_get_response.assert_called_with(
            url=f"https://understat.com/player/{self.player_id}",
            query="groupsData",
        )

    def test_team_get_player_data(
        self, mock_get_response, mock_get, mock_request_url
    ):
        """ test ``team.get_player_data()`` """
        self.team.get_player_data(season="2019")
        mock_get_response.assert_called_with(
            url=f"https://understat.com/team/{self.team_name}/2019",
            query="playersData",
        )

    def test_team_get_match_data(
        self, mock_get_response, mock_get, mock_request_url
    ):
        """ test ``team.get_match_data()`` """
        self.team.get_match_data(season="2019")
        mock_get_response.assert_called_with(
            url=f"https://understat.com/team/{self.team_name}/2019",
            query="datesData",
        )

    def test_get_context_data_args(
        self, mock_get_response, mock_get, mock_request_url
    ):
        """ test ``team.get_match_data()`` """
        self.team.get_context_data(season="2019")
        mock_get_response.assert_called_with(
            url=f"https://understat.com/team/{self.team_name}/2019",
            query="statisticsData",
        )

    def test_league_get_team_data(
        self, mock_get_response, mock_get, mock_request_url
    ):
        """ test ``league.get_team_data()`` """
        self.league.get_team_data(season="2019")
        mock_get_response.assert_called_with(
            url=f"https://understat.com/league/{self.league_name}/2019",
            query="teamsData",
        )

    def test_league_get_match_data(
        self, mock_get_response, mock_get, mock_request_url
    ):
        """ test ``league.get_match_data()`` """
        self.league.get_match_data(season="2019")
        mock_get_response.assert_called_with(
            url=f"https://understat.com/league/{self.league_name}/2019",
            query="datesData",
        )

    def test_league_getplayer_data(
        self, mock_get_response, mock_get, mock_request_url
    ):
        """ test ``league.get_player_data()`` """
        self.league.get_player_data(season="2019")
        mock_get_response.assert_called_with(
            url=f"https://understat.com/league/{self.league_name}/2019",
            query="playersData",
        )


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

    def test_get_data_type_error(self, mock_get):
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

    def test_get_data_type_error(self, mock_get):
        """
        test that ``league._get_data()`` raises a TypeError
        when ``league`` is not a string
        """
        league = self.understat.league(None)
        with self.assertRaises(TypeError):
            _ = league.get_match_data(season="2019")


class TestEndpointDunder(EndpointBaseTestCase):
    """Tests for the dunder methods in the endpoint class"""

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


if __name__ == "__main__":
    unittest.main()