""" Define custom exceptions """
from typing import Optional, Union, List

PrimaryAttribute = Union[List[str], str]


class InvalidQuery(Exception):
    """ Query gets no response """

    def __init__(self, *args: Optional[PrimaryAttribute]) -> None:
        if args:
            self.message = (
                f"There is no html entry matching the query {args[0]}"
            )
        else:
            self.message = "There is not html entry matching the given query"

    def __str__(self) -> str:
        return self.message


class InvalidSeason(Exception):
    """ Invalid season """

    def __init__(self, *args: Optional[PrimaryAttribute]) -> None:
        if args:
            self.message = f"{args[0]} is not a valid season"
        else:
            self.message = "The value passed to `season` is not valid"

    def __str__(self) -> str:
        return self.message


class InvalidPlayer(Exception):
    """ Invalid player """

    def __init__(self, *args: Optional[PrimaryAttribute]) -> None:
        if args:
            self.message = f"{args[0]} is not a valid player or player id"
        else:
            self.message = "The value passed to `player` is not valid"

    def __str__(self) -> str:
        return self.message


class InvalidLeague(Exception):
    """ Invalid league """

    def __init__(self, *args: Optional[PrimaryAttribute]) -> None:
        if args:
            self.message = f"{args[0]} is not a valid league"
        else:
            self.message = "The value passed to `league` is not valid"

    def __str__(self) -> str:
        return self.message


class InvalidTeam(Exception):
    """ Invalid team """

    def __init__(self, *args: Optional[PrimaryAttribute]) -> None:
        if args:
            self.message = f"{args[0]} is not a valid team"
        else:
            self.message = "The value passed to `team` is not valid"

    def __str__(self) -> str:
        return self.message


class InvalidMatch(Exception):
    """ Invalid match """

    def __init__(self, *args: Optional[PrimaryAttribute]) -> None:
        if args:
            self.message = f"{args[0]} is not a valid match"
        else:
            self.message = "The value passed to `match` is not valid"

    def __str__(self) -> str:
        return self.message
