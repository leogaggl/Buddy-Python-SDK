import datetime
import easysettings
import unittest
from buddysdk import Settings
import TestBase

class Test_test3(TestBase.TestBase):
   
    _app_id = "a"
    _default_service_root = "https://api.buddyplatform.com"
    _service_root = "sr"
    _access_token = "at"

    def test_Settings_empty(self):
        settings = Settings.Settings(Test_test3._app_id)
        self.assertEqual(settings.access_token, "")
        self.assertEqual(settings.service_root, Test_test3._default_service_root)
    
    def test_Settings_access_token(self):
        settings = Settings.Settings(Test_test3._app_id)

        now = datetime.datetime.now(datetime.timezone.utc)
        future = now + datetime.timedelta(1)
        json = {"accessToken": Test_test3._access_token, "accessTokenExpires": self.javascript_datetime_from_datetime(future), "serviceRoot": Test_test3._service_root}
        settings.process_device_registration(json)
        self.assertEqual(settings.access_token, Test_test3._access_token)

    def test_Settings_access_token_expired(self):
        settings = Settings.Settings(Test_test3._app_id)

        now = datetime.datetime.now(datetime.timezone.utc)
        past = now - datetime.timedelta(1)
        json = {"accessToken": Test_test3._access_token, "accessTokenExpires": self.javascript_datetime_from_datetime(past), "serviceRoot": Test_test3._service_root}
        settings.process_device_registration(json)
        self.assertEqual(settings.access_token, "")

    def test_Settings_save_load(self):

        # pre-load Settings with a different test
        self.test_Settings_access_token()

        settings = Settings.Settings(Test_test3._app_id)

        self.assertEqual(settings.access_token, Test_test3._access_token)
        self.assertEqual(settings.service_root, Test_test3._service_root)

if __name__ == '__main__':
    unittest.main()
