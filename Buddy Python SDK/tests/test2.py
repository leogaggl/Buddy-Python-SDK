import unittest

import Buddy
import TestBase


class test_test2(TestBase.TestBase):
    def test_Buddy_init(self):
        client_a = Buddy.Buddy.init("a", "b")
        self.assertEqual(client_a.app_id, "a")
        self.assertEqual(client_a.app_key, "b")

    def test_Buddy_init_multiple(self):
        client_1 = Buddy.Buddy.init("a", "b")
        self.assertEqual(client_1.app_id, "a")
        self.assertEqual(client_1.app_key, "b")
        
        client_2 = Buddy.Buddy.init("c", "d")
        self.assertEqual(client_2.app_id, "c")
        self.assertEqual(client_2.app_key, "d")

        self.assertEqual(Buddy.Buddy.current_client.app_id, "c")
        self.assertEqual(Buddy.Buddy.current_client.app_key, "d")

        self.assertEqual(Buddy.Buddy.current_client, client_2)

if __name__ == '__main__':
    unittest.main()
