import unittest
import datetime
import easysettings
from buddysdk import Settings


class Test_test3(unittest.TestCase):
    def test_Settings_access_token(self):
        es = easysettings.EasySettings("buddy.conf")
        es.clear()

        settings = Settings.Settings("a")

        now = datetime.datetime.now(datetime.timezone.utc)
        future = now + datetime.timedelta(1)
        json = [{"accessToken": "at", "accessTokenExpires": str(round(future.timestamp() * 1000)), "serviceRoot": "sr"}]
        settings.process_device_registration(json)
        self.assertEqual(settings.get_access_token(), "at")

    def test_Settings_access_token_expired(self):
        es = easysettings.EasySettings("buddy.conf")
        es.clear()

        settings = Settings.Settings("a")

        now = datetime.datetime.now(datetime.timezone.utc)
        past = now - datetime.timedelta(1)
        json = [{"accessToken": "at", "accessTokenExpires": str(round(past.timestamp() * 1000)), "serviceRoot": "sr"}]
        settings.process_device_registration(json)
        self.assertEqual(settings.get_access_token(), None)

if __name__ == '__main__':
    unittest.main()
