import buddy
from test_base import TestBase


class Test2(TestBase):
    def test_buddy_init(self):
        client = buddy.https("a", "b")
        self.assertEqual(buddy.app_id, "a")
        self.assertEqual(buddy.https, client)

    def test_buddy_init_multiple(self):
        buddy.https("ai", "ak")
        self.assertEqual(buddy.https_client.settings.app_id, "ai")
        self.assertEqual(buddy.https_client.settings.app_key, "ak")

        self.reset_module()
        client_2 = buddy.https("bi", "bk")
        self.assertEqual(client_2.settings.app_id, "bi")
        self.assertEqual(client_2.settings.app_key, "bk")

        self.assertEqual(buddy.app_id, "bi")

        self.assertEqual(buddy.https, client_2)


if __name__ == '__main__':
    unittest.main()
