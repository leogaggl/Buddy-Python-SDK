import unittest
from buddy import Buddy
from settings import Settings
from test_base import TestBase


class Test_test4(TestBase):

    def test_register_device_us(self):

        self.register_device(self, TestBase.US_app_id, TestBase.US_app_key, "https://api")

    def test_register_device_eu(self):

        self.register_device(self, TestBase.EU_app_id, TestBase.EU_app_key, "https://api-eu")

    def register_device(self, test, app_id, app_key, service_root_starts_with):
        self.setup_with_bad_device_token()

        client = Buddy.init(app_id, app_key)

        access_token_string = client.get_access_token_string()

        settings = Settings(app_id)
        test.assertEqual(access_token_string, settings.access_token_string)
        test.assertTrue(settings.service_root.startswith(service_root_starts_with))


if __name__ == '__main__':
    unittest.main()
