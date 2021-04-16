""" understatAPI client """
from types import TracebackType
from typing import Iterator
import requests
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

    def __init__(self, session: requests.Session = None) -> None:
        """
        :session: An existing `requests` session
        """
        self.session = session or requests.Session()

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
        """ League endpoint """
        return LeagueEndpoint(league=league, session=self.session)

    def player(self, player: PrimaryAttribute) -> PlayerEndpoint:
        """ Player endpoint """
        return PlayerEndpoint(player=player, session=self.session)

    def team(self, team: PrimaryAttribute) -> TeamEndpoint:
        """ Team endpoint """
        return TeamEndpoint(team=team, session=self.session)

    def match(self, match: PrimaryAttribute) -> MatchEndpoint:
        """ Match endpoint """
        return MatchEndpoint(match=match, session=self.session)

    def search(
        self, player_name: str, **kwargs: int
    ) -> Iterator[PlayerEndpoint]:
        """ Search for a player or players """
        with Search(
            player_name=player_name, session=self.session, **kwargs
        ) as search:
            for player in search.get_player_ids():
                yield PlayerEndpoint(player, session=self.session)
