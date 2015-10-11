import unittest
import datetime
import easysettings
import TestBase
from buddysdk import Settings

class Test_test3(TestBase.TestBase):
   
    def test_Settings_empty(self):
        settings = Settings.Settings("a")
        self.assertEqual(settings.access_token, "")
        self.assertEqual(settings.service_root, "https://api.buddyplatform.com")
    
    def test_Settings_access_token(self):
        settings = Settings.Settings("a")

        now = datetime.datetime.now(datetime.timezone.utc)
        future = now + datetime.timedelta(1)
        json = {"accessToken": "at", "accessTokenExpires": self.convert_datetime_to_ticks(future), "serviceRoot": "sr"}
        settings.process_device_registration(json)
        self.assertEqual(settings.access_token, "at")

    def test_Settings_access_token_expired(self):
        settings = Settings.Settings("a")

        now = datetime.datetime.now(datetime.timezone.utc)
        past = now - datetime.timedelta(1)
        json = {"accessToken": "at", "accessTokenExpires": self.convert_datetime_to_ticks(past), "serviceRoot": "sr"}
        settings.process_device_registration(json)
        self.assertEqual(settings.access_token, "")

if __name__ == '__main__':
    unittest.main()
