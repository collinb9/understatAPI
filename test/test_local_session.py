"""
Test the API when you use ``understat.session.LocalSession`` instead of
``requests.session``
"""
import unittest
from understatapi import UnderstatClient
from understatapi.session import LocalSession


class TestLocalSession(unittest.TestCase):
    """Test out the local session"""

    def setUp(self):
        self.api = UnderstatClient(session=LocalSession)

    def tearDown(self):
        self.api.session.close()

    def test_dummy(self):
        print("Hello world!")
