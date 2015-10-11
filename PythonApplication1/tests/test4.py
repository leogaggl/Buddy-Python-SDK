﻿import easysettings
import unittest
from buddysdk import Settings
from buddysdk import Buddy
import TestBase

class Test_test4(TestBase.TestBase):

    def test_register_device_us(self):

        TestHelper().register_device(self, TestBase.TestBase.US_app_id, TestBase.TestBase.US_app_key, "https://api")

    def test_register_device_eu(self):

        TestHelper().register_device(self, TestBase.TestBase.EU_app_id, TestBase.TestBase.EU_app_key, "https://api-eu")


class TestHelper(object):
    def register_device(self, test, app_id, app_key, service_root_starts_with):

        settings = Settings.Settings(app_id)
        client = Buddy.Buddy.init(app_id, app_key, settings)

        client.register_device()

        test.assertIsNotNone(settings.access_token)
        test.assertTrue(settings.service_root.startswith(service_root_starts_with))


if __name__ == '__main__':
    unittest.main()
