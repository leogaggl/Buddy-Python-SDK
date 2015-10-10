import unittest
from buddysdk import BuddyClient
from buddysdk import Settings

class test_test1(unittest.TestCase):
    def test_BuddyClient(self):
        client = BuddyClient.BuddyClient("a", "b", Settings.Settings("a"))
        self.assertIsNotNone(client)

if __name__ == '__main__':
    unittest.main()
