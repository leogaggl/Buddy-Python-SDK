import unittest

from buddy_client import BuddyClient
from test_base import TestBase


class test_test1(TestBase):

    def test_BuddyClient(self):
        client = BuddyClient(TestBase.US_app_id, TestBase.US_app_key)
        self.assertIsNotNone(client)
        self.assertIs(client.app_id, TestBase.US_app_id);
        self.assertIs(client.app_key, TestBase.US_app_key);


if __name__ == '__main__':
    unittest.main()
