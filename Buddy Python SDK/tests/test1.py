import unittest

from BuddyClient import BuddyClient
from Settings import Settings
from TestBase import TestBase


class test_test1(TestBase):

    def test_BuddyClient(self):
        client = BuddyClient(TestBase.US_app_id, TestBase.US_app_key, Settings(test_test1.US_app_id))
        self.assertIsNotNone(client)
        self.assertIs(client.app_id, TestBase.US_app_id);
        self.assertIs(client.app_key, TestBase.US_app_key);

if __name__ == '__main__':
    unittest.main()
