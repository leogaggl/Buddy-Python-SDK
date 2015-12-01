import unittest

from buddy import Buddy
from test_base import TestBase


class test_test2(TestBase):
    def test_Buddy_init(self):
        client_a = Buddy.init("a", "b")
        self.assertEqual(client_a.app_id, "a")
        self.assertEqual(client_a.app_key, "b")

    def test_Buddy_init_multiple(self):
        client_1 = Buddy.init("a", "b")
        self.assertEqual(client_1.app_id, "a")
        self.assertEqual(client_1.app_key, "b")
        
        client_2 = Buddy.init("c", "d")
        self.assertEqual(client_2.app_id, "c")
        self.assertEqual(client_2.app_key, "d")

        self.assertEqual(Buddy.current_client.app_id, "c")
        self.assertEqual(Buddy.current_client.app_key, "d")

        self.assertEqual(Buddy.current_client, client_2)


if __name__ == '__main__':
    unittest.main()
