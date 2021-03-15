""" Team endpoint """
from .base import BaseEndpoint


class TeamEndpoint(BaseEndpoint):
    """
    Use this class to get data from a url of the form
    https://understat.com/player/<team>/<season>
    """

    queries = ["matchesData", "shotsData", "groupsData"]
