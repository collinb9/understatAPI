""" Define custom exceptions """
from typing import Union, List

PrimaryAttribute = Union[List[str], str]


class InvalidSeason(Exception):
    """ Invalid season """

    def __init__(self, message: str, season: str) -> None:
        super().__init__(message)
        self.season = season


class InvalidPlayer(Exception):
    """ Invalid player """

    def __init__(self, message: str, player: str) -> None:
        super().__init__(message)
        self.player = player


class InvalidLeague(Exception):
    """ Invalid league """

    def __init__(self, message: str, league: str) -> None:
        super().__init__(message)
        self.league = league


class InvalidTeam(Exception):
    """ Invalid team """

    def __init__(self, message: str, team: str) -> None:
        super().__init__(message)
        self.team = team


class InvalidMatch(Exception):
    """ Invalid match """

    def __init__(self, message: str, match: str) -> None:
        super().__init__(message)
        self.match = match
