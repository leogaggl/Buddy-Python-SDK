import buddy
from test_base import TestBase


class Test2(TestBase):
    def test_buddy_init(self):
        buddy.init_https("a", "b")
        self.assertEqual(buddy.app_id, "a")

    def test_buddy_init_multiple(self):
        client_1 = buddy.init_https("ai", "ak")
        self.assertEqual(client_1.settings.app_id, "ai")
        self.assertEqual(client_1.settings.app_key, "ak")
        
        client_2 = buddy.init_https("bi", "bk")
        self.assertEqual(client_2.settings.app_id, "bi")
        self.assertEqual(client_2.settings.app_key, "bk")

        self.assertEqual(buddy.app_id, "bi")

        self.assertEqual(buddy.https, client_2)


if __name__ == '__main__':
    unittest.main()
