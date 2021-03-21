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
        self.league = LeagueEndpoint(self.session)
        self.player = PlayerEndpoint(self.session)
        self.team = TeamEndpoint(self.session)
        self.match = MatchEndpoint(self.session)

    def __enter__(self) -> "UnderstatClient":
        return self

    def __exit__(
        self,
        exception_type: type,
        exception_value: BaseException,
        traceback: TracebackType,
    ) -> None:
        self.session.close()
