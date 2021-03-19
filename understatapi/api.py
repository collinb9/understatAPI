""" understatAPI client """
from .endpoints import (
    LeagueEndpoint,
    PlayerEndpoint,
    TeamEndpoint,
    MatchEndpoint,
)


class APIClient:
    """ API client for understat """

    def __init__(self) -> None:
        """ Initialise APIClient """
        self.league = LeagueEndpoint()
        self.player = PlayerEndpoint()
        self.team = TeamEndpoint()
        self.match = MatchEndpoint()
