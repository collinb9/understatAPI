""" understatAPI client """
from types import TracebackType
from typing import Iterator
import requests
from selenium.common.exceptions import WebDriverException
from .utils import get_public_methods, str_to_class, find_endpoints
from .endpoints import (
    LeagueEndpoint,
    PlayerEndpoint,
    TeamEndpoint,
    MatchEndpoint,
)
from .services import Search
from .exceptions import PrimaryAttribute


class UnderstatClient:
    """#pylint: disable=line-too-long
    API client for understat

    The main interface for interacting with understatAPI. Exposes
    each of the entrypoints and services, maintains a consistent
    session and handles errors

    :Example:

    .. code-block::

        from understatapi import UnderstatClient

        with UnderstatClient() as understat:
            league_player_data = understat.league(league="EPL").get_player_data(season="2019")
            player_shot_data = understat.player(player="2371").get_shot_data()
            team_match_data = understat.team(team="Manchester_United").get_match_data(season="2019")
            roster_data = understat.match(match="14711").get_roster_data()
            player_match_data = understat.search("Cristiano Ronaldo").get_match_data()

    Using the context manager gives some more verbose error handling

    .. testsetup::

            from understatapi import UnderstatClient

    .. doctest::

        >>> team=""
        >>> with UnderstatClient() as understat:
        ...     understat.team(team).get_bad_data() # doctest: +SKIP
        Traceback (most recent call last)
        File "<stdin>", line 2, in <module>
        File "understatapi/api.py", line 59, in __exit__
            raise AttributeError(
        AttributeError: 'TeamEndpoint' object has no attribute 'get_bad_data'
        Its public methods are ['get_context_data', 'get_match_data', 'get_player_data']

    """

    def __init__(self) -> None:
        self.session = requests.Session()

    def __enter__(self) -> "UnderstatClient":
        return self

    def __exit__(
        self,
        exception_type: type,
        exception_value: BaseException,
        traceback: TracebackType,
    ) -> None:
        if exception_type is AttributeError:
            endpoint = find_endpoints(str(exception_value))
            endpoint_obj = str_to_class(__name__, endpoint[0])
            public_methods = get_public_methods(endpoint_obj)
            raise AttributeError(
                str(exception_value)
                + f"\nIts public methods are {public_methods}"
            )
        self.session.close()

    def league(self, league: PrimaryAttribute) -> LeagueEndpoint:
        """
        Endpoint for league data. Use this function to get data from a
        url of the form ``https://understat.com/league/<league>/<season>``

        :param league: Name of the league(s) to get data for,
            one of {EPL, La_Liga, Bundesliga, Serie_A, Ligue_1, RFPL}
        :rtype: :py:class:`~understatapi.endpoints.league.LeagueEndpoint`

        :Example:

        .. testsetup::

            from understatapi import UnderstatClient

        .. doctest::

            >>> leagues = ["EPL", "Bundesliga"]
            >>> with UnderstatClient() as understat:
            ...     for league in understat.league(leagues):
            ...         print(league.league)
            EPL
            Bundesliga

        """
        return LeagueEndpoint(league=league, session=self.session)

    def player(self, player: PrimaryAttribute) -> PlayerEndpoint:
        """
        Endpoint for player data. Use this function to get data from a
        url of the form ``https://understat.com/player/<player_id>/``

        :param player: Id of the player(s) to get data for
        :rtype: :py:class:`~understatapi.endpoints.player.PlayerEndpoint`

        :Example:

        .. testsetup::

            from understatapi import UnderstatClient

        .. doctest::

            >>> player_ids = ["000", "111"]
            >>> with UnderstatClient() as understat:
            ...     for player in understat.player(player_ids):
            ...         print(player.player)
            000
            111

        """
        return PlayerEndpoint(player=player, session=self.session)

    def team(self, team: PrimaryAttribute) -> TeamEndpoint:
        """
        Endpoint for team data. Use this function to get data from a
        url of the form ``https://understat.com/team/<team>/<season>``

        :param team: Name of the team(s) to get data for
        :rtype: :py:class:`~understatapi.endpoints.team.TeamEndpoint`

        :Example:

        .. testsetup::

            from understatapi import UnderstatClient

        .. doctest::

            >>> team_names = ["Manchester_United", "Liverpool"]
            >>> with UnderstatClient() as understat:
            ...     for team in understat.team(team_names):
            ...         print(team.team)
            Manchester_United
            Liverpool

        """
        return TeamEndpoint(team=team, session=self.session)

    def match(self, match: PrimaryAttribute) -> MatchEndpoint:
        """
        Endpoint for match data. Use this function to get data from a
        url of the form ``https://understat.com/match/<match_id>``

        :param match: Id of match(es) to get data for
        :rtype: :class:`~understatapi.endpoints.match.MatchEndpoint`

        :Example:

        .. testsetup::

            from understatapi import UnderstatClient

        .. doctest::

            >>> match_ids = ["123", "456"]
            >>> with UnderstatClient() as understat:
            ...     for match in understat.match(match_ids):
            ...         print(match.match)
            123
            456

        """
        return MatchEndpoint(
            match=match,
            session=self.session,
        )

    def search(
        self, player_name: str, max_ids: int = 5, page_load_timeout: int = 5
    ) -> Iterator[PlayerEndpoint]:
        """#pylint: disable=line-too-long
        Search for a player by name

        :param player_name: Player name to enter into the
            seach bar
        :param max_ids: The maximum number of player ids to return
        :param page_load_timeout: Number of seconds to wait for the page
            to load before raising a ``TimeoutError``
        :rtype: :class:`Iterator` [:class:`~understatapi.endpoints.player.PlayerEndpoint`]


        :Example:

        .. testsetup::

            from minimock import Mock
            from understatapi import UnderstatClient
            from understatapi.endpoints import PlayerEndpoint
            from understatapi.services import Search
            players = [[
                "2371",
                "2028",
                "7097",
                ],
                ["2371"]
            ]
            Search.get_player_ids = Mock(
                "Search.get_player_ids",
                returns_iter=players,
                tracker=None
            )

        .. doctest::

            >>> player_name = "Ronaldo"
            >>> with UnderstatClient() as understat:
            ...     for player in understat.search(player_name):
            ...         print(player.player)
            2371
            2028
            7097
            >>> with UnderstatClient() as understat:
            ...     for player in understat.search(player_name, max_ids=1):
            ...         print(player.player)
            2371

        """
        try:
            with Search(
                player_name=player_name,
                session=self.session,
                max_ids=max_ids,
                page_load_timeout=page_load_timeout,
            ) as search:
                for player in search.get_player_ids():
                    yield PlayerEndpoint(player=player, session=self.session)
        except WebDriverException as err:
            raise WebDriverException(
                "You must have 'geckodriver' installed to "
                "use UnderstatClient.search()"
            ) from err
