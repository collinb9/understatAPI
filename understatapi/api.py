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

        self.session = None
        self.args = args
        self.kwargs = kwargs

    def __enter__(self):
        pass

    def __exit__(self, exception_type, exception_value, traceback):
        pass
