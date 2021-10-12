""" Base endpoint """
from typing import Sequence
import requests
from requests import Response
from ..parsers import BaseParser
from ..exceptions import (
    InvalidLeague,
    InvalidSeason,
    PrimaryAttribute,
)


class BaseEndpoint:
    """
    Base endpoint for understat API

    :attr base_url: str: The base url to use for requests,
        ``https://understat.com/``
    :attr leagues: List[str]: The available leagues, ``EPL``, ``La_Liga``,
        ``Bundesliga``, optional``Serie_A``, ``Ligue_1``, ``RFPL``
    """

    base_url = "https://understat.com/"
    leagues = ["EPL", "La_Liga", "Bundesliga", "Serie_A", "Ligue_1", "RFPL"]
    parser: BaseParser

    def __init__(
        self,
        primary_attr: PrimaryAttribute,
        session: requests.Session,
    ) -> None:
        """
        :session: requests.Session: The current ``request`` session
        """
        self.session = session
        self._primary_attr = primary_attr

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self._primary_attr!r})>"

    def __len__(self) -> int:
        if isinstance(self._primary_attr, str):
            return 1
        if isinstance(self._primary_attr, Sequence):
            return len(self._primary_attr)
        raise TypeError("Primary attribute is not a sequence or string")

    def __getitem__(self, index: int) -> "BaseEndpoint":
        if index >= len(self):
            raise IndexError
        if isinstance(self._primary_attr, str):
            return self.__class__(self._primary_attr, session=self.session)
        return self.__class__(self._primary_attr[index], session=self.session)

    def _check_args(self, league: str = None, season: str = None) -> None:
        """ Handle invalid arguments """
        if league is not None and league not in self.leagues:
            raise InvalidLeague(
                f"{league}is not a valid league", league=league
            )
        if season is not None and int(season) < 2014:
            raise InvalidSeason(
                f"{season} is not a valid season", season=season
            )

    def _request_url(self, *args: str, **kwargs: str) -> Response:
        """
        Use the requests module to send a HTTP request to a url, and check
        that this request worked.

        :param args: Arguments to pass to ``requests.get()``
        :param kwargs: Keyword arguments to pass to ``requests.get()``
        """
        res = self.session.get(*args, **kwargs)
        res.raise_for_status()
        return res
