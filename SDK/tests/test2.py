import unittest

import buddy
from test_base import TestBase


class Test2(TestBase):
    def test_buddy_init(self):
        client_a = buddy.init("a", "b")
        self.assertEqual(client_a.app_id, "a")
        self.assertEqual(client_a.app_key, "b")

    def test_buddy_init_multiple(self):
        client_1 = buddy.init("a", "b")
        self.assertEqual(client_1.app_id, "a")
        self.assertEqual(client_1.app_key, "b")
        
        client_2 = buddy.init("c", "d")
        self.assertEqual(client_2.app_id, "c")
        self.assertEqual(client_2.app_key, "d")

        self.assertEqual(buddy.current_client.app_id, "c")
        self.assertEqual(buddy.current_client.app_key, "d")

        self.assertEqual(buddy.current_client, client_2)


if __name__ == '__main__':
    unittest.main()
