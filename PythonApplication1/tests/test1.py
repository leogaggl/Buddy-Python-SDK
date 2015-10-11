import unittest
from buddysdk import BuddyClient
from buddysdk import Settings
import TestBase

class test_test1(TestBase.TestBase):

    def test_BuddyClient(self):
        client = BuddyClient.BuddyClient("a", "b", Settings.Settings("a"))
        self.assertIsNotNone(client)

if __name__ == '__main__':
    unittest.main()
