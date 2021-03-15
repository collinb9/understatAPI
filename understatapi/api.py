""" understatAPI client """
from .endpoints import LeagueEndpoint, PlayerEndpoint


class APIClient:
    """ API client for understat """

    def __init__(self):
        """ Initialise APIClient """
        self.league = LeagueEndpoint()
        self.player = PlayerEndpoint()
