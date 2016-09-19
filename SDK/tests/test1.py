import unittest

from buddy_events import BuddyEvents
from https import Https
from settings import Settings
from test_base import TestBase


class Test1(TestBase):

    def test_Https(self):
        settings = Settings(TestBase.US_app_id, TestBase.US_app_key)
        events = BuddyEvents()
        client = Https(events, settings)
        self.assertIsNotNone(client)
        self.assertIs(settings.app_id, TestBase.US_app_id)
        self.assertIs(settings.app_key, TestBase.US_app_key)


if __name__ == '__main__':
    unittest.main()
