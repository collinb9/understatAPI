""" Define custom exceptions """
from typing import Optional


class InvalidQuery(Exception):
    """ Query gets no response """

    def __init__(self, *args: Optional[str]) -> None:
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

    def __init__(self, *args: str) -> None:
        if args:
            self.message = f"{args[0]} is not a valid season"
        else:
            self.message = "The value of passed to `season` is not valid"

    def __str__(self) -> str:
        return self.message


class InvalidPlayer(Exception):
    """ Invalid player """

    def __init__(self, *args: str) -> None:
        if args:
            self.message = f"{args[0]} is not a valid player or player id"
        else:
            self.message = "The value of passed to `player` is not valid"

    def __str__(self) -> str:
        return self.message


class InvalidLeague(Exception):
    """ Invalid league """

    def __init__(self, *args: str) -> None:
        if args:
            self.message = f"{args[0]} is not a valid league"
        else:
            self.message = "The value of passed to `league` is not valid"

    def __str__(self) -> str:
        return self.message
