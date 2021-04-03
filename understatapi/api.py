""" understatAPI client """
from types import TracebackType
from typing import Iterator
import requests
from selenium.common.exceptions import WebDriverException
from .endpoints import (
    LeagueEndpoint,
    PlayerEndpoint,
    TeamEndpoint,
    MatchEndpoint,
)
from .services import Search
from .exceptions import PrimaryAttribute


class UnderstatClient:
    """ API client for understat """

    def __init__(self) -> None:
        self.session = requests.Session()

    def __enter__(self) -> "UnderstatClient":
        return self

    def __exit__(
        self,
        exception_type: type,
        exception_value: BaseException,
        traceback: TracebackType,
    ) -> None:
        self.session.close()

    def league(self, league: PrimaryAttribute) -> LeagueEndpoint:
        """
        League endpoint

        :param league: str: Name of the league(s) to get data for,
            one of {EPL, La_Liga, Bundesliga, Serie_A, Ligue_1, RFPL}

        :return: LeagueEndpoint: The endpoint for getting data from a
            url of the form https://understat.com/league/<league>/<season>
        """
        return LeagueEndpoint(league=league, session=self.session)

    def player(self, player: PrimaryAttribute) -> PlayerEndpoint:
        """
        Player endpoint

        :param player: PrimaryAttribute: Understat id of the player(s) to
            get data for

        :return: PlayerEndpoint: The endpoint for getting data from a url
            of the form https://understat.com/player/<player_id>/
        """
        return PlayerEndpoint(player=player, session=self.session)

    def team(self, team: PrimaryAttribute) -> TeamEndpoint:
        """
        Team endpoint

        :param team: PrimaryAttribute: Name of the team(s) to get data for

        :return: TeamEndpoint: The endpoint for getting data from a url of
            the form https://understat.com/team/<team>/<season>
        """
        return TeamEndpoint(team=team, session=self.session)

    def match(self, match: PrimaryAttribute) -> MatchEndpoint:
        """
        Match endpoint

        :param match: PrimaryAttribute: Id of match(s) to get data for

        :return: MatchEndpoint: The endpoint for getting data from a url of
            the form https://understat.com/match/<match_id>
        """
        return MatchEndpoint(match=match, session=self.session)

    def search(
        self, player_name: str, max_ids: int = 5, page_load_timeout: int = 5
    ) -> Iterator[PlayerEndpoint]:
        """
        Search for a player by name

        :param player_name: PrimaryAttribute: Player name to enter into the
            seach bar
        :max_ids: int: The maximum number of player ids to return
        :page_load_timeout: int: Number of seconds to wait for the page
            to load before raising a `TimeoutError`

        :yield: PlayerEndpoint: The endpoint for getting data from a url
            of the form https://understat.com/player/<player_id>/
        """
        try:
            with Search(
                player_name=player_name,
                session=self.session,
                max_ids=max_ids,
                page_load_timeout=page_load_timeout,
            ) as search:
                for player in search.get_player_ids():
                    yield PlayerEndpoint(player=player, session=self.session)
        except WebDriverException as err:
            raise WebDriverException(
                "You must have 'geckodriver' installed to "
                "use UnderstatClient.search()"
            ) from err
