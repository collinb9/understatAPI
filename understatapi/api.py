""" understatAPI client """
from types import TracebackType
import requests
from .endpoints import (
    LeagueEndpoint,
    PlayerEndpoint,
    TeamEndpoint,
    MatchEndpoint,
)


class UnderstatClient:
    """ API client for understat """

    def __init__(self) -> None:
        """ Initialise APIClient """
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

    def league(self, league: str) -> LeagueEndpoint:
        """ League endpoint """
        return LeagueEndpoint(league=league, session=self.session)

    def player(self, player: str) -> PlayerEndpoint:
        """ Player endpoint """
        return PlayerEndpoint(player=player, session=self.session)

    def team(self, team: str) -> TeamEndpoint:
        """ Team endpoint """
        return TeamEndpoint(team=team, session=self.session)

    def match(self, match: str) -> MatchEndpoint:
        """ Match endpoint """
        return MatchEndpoint(match=match, session=self.session)
