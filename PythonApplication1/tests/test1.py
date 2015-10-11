import unittest
import TestBase
from buddysdk import BuddyClient
from buddysdk import Settings

class test_test1(TestBase.TestBase):
    def test_BuddyClient(self):
        client = BuddyClient.BuddyClient("a", "b", Settings.Settings("a"))
        self.assertIsNotNone(client)

if __name__ == '__main__':
    unittest.main()
