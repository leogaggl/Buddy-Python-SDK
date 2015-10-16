import unittest

import BuddyClient
import Settings
import TestBase


class test_test1(TestBase.TestBase):

    def test_BuddyClient(self):
        client = BuddyClient.BuddyClient(TestBase.TestBase.US_app_id, TestBase.TestBase.US_app_key, Settings.Settings(test_test1.US_app_id))
        self.assertIsNotNone(client)
        self.assertIs(client.app_id, TestBase.TestBase.US_app_id);
        self.assertIs(client.app_key, TestBase.TestBase.US_app_key);

if __name__ == '__main__':
    unittest.main()
