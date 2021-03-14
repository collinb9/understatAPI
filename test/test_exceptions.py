""" Tests for custom exceptions """
import unittest
from understatapi.exceptions import (
    InvalidQuery,
    InvalidLeague,
    InvalidSeason,
    InvalidPlayer,
)


class TestInvalidQuery(unittest.TestCase):
    """ Test InvalidQuery """

    def test_default(self):
        """ test InvalidQuery with no message """
        with self.assertRaisesRegex(
            InvalidQuery, "There is not html entry matching the given query"
        ):
            raise InvalidQuery

    def test_message(self):
        """ test InvalidQuery with a message """
        with self.assertRaisesRegex(
            InvalidQuery,
            "There is no html entry matching the query invalidQuery",
        ):
            raise InvalidQuery("invalidQuery")


class TestInvalidSeason(unittest.TestCase):
    """ Test InvalidSeason """

    def test_default(self):
        """ test InvalidSeason with no message """
        with self.assertRaisesRegex(
            InvalidSeason, "The value of passed to `season` is not valid"
        ):
            raise InvalidSeason

    def test_message(self):
        """ test InvalidSeason with a message """
        with self.assertRaisesRegex(
            InvalidSeason,
            "1999 is not a valid season",
        ):
            raise InvalidSeason("1999")


class TestInvalidPlayer(unittest.TestCase):
    """ Test InvalidPlayer """

    def test_default(self):
        """ test InvalidPlayer with no message """
        with self.assertRaisesRegex(
            InvalidPlayer, "The value of passed to `player` is not valid"
        ):
            raise InvalidPlayer

    def test_message(self):
        """ test InvalidPlayer with a message """
        with self.assertRaisesRegex(
            InvalidPlayer,
            "Player is not a valid player or player id",
        ):
            raise InvalidPlayer("Player")


class TestInvalidLeague(unittest.TestCase):
    """ Test InvalidLeague """

    def test_default(self):
        """ test InvalidLeague with no message """
        with self.assertRaisesRegex(
            InvalidLeague, "The value of passed to `league` is not valid"
        ):
            raise InvalidLeague

    def test_message(self):
        """ test InvalidLeague with a message """
        with self.assertRaisesRegex(
            InvalidLeague,
            "League is not a valid league",
        ):
            raise InvalidLeague("League")


if __name__ == "__main__":
    unittest.main()
