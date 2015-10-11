import easysettings
import TestBase
import unittest
from buddysdk import Settings
from buddysdk import Buddy

class Test_test4(TestBase.TestBase):
    def test_register_device_us(self):

        TestHelper().register_device(self, "bbbbbc.xgjbvPdwkllw", "1E9E824E-A3F1-4F34-B4F4-9CC87471A564", "https://api")


class TestHelper(object):
    def register_device(self, test, app_id, app_key, service_root_starts_with):

        settings = Settings.Settings(app_id)
        client = Buddy.Buddy.init(app_id, app_key, settings)

        client.register_device()

        test.assertIsNotNone(settings.access_token)
        test.assertTrue(settings.service_root.startswith(service_root_starts_with))


if __name__ == '__main__':
    unittest.main()
