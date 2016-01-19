import unittest

from access_token import AccessToken
from settings import Settings
from test_base import TestBase


class Test3(TestBase):

    _app_id = "a"
    _default_service_root = "https://api.buddyplatform.com"
    _service_root = "sr"
    _access_token = "at"

    def test_Settings_empty(self):
        settings = Settings(Test3._app_id)
        at = settings.access_token_string
        self.assertEqual(at, None)
        self.assertEqual(settings.service_root, Test3._default_service_root)

    def test_access_token(self):
        future = self.access_token_base(1)
        self.assertEqual(future.token, Test3._access_token)

    def test_access_token_expired(self):
        past = self.access_token_base(-1)
        self.assertEqual(past.token, None)

    def access_token_base(self, days):
        datetime = self.datetime_from_days(days)
        at = AccessToken([Test3._access_token, str(self.ticks_from_datetime(datetime))])
        return at

    def test_Settings_access_token(self):
        settings = Settings(Test3._app_id)

        json = {"accessToken": Test3._access_token,
                "accessTokenExpires": self.future_javascript_access_token_expires(),
                "serviceRoot": Test3._service_root}

        settings.set_device_token(json)

        self.assertEqual(settings.access_token_string, Test3._access_token)

    def test_Settings_access_token_expired(self):
        settings = Settings(Test3._app_id)

        json = {"accessToken": Test3._access_token,
                "accessTokenExpires": self.past_javascript_access_token_expires(),
                "serviceRoot": Test3._service_root}

        settings.set_device_token(json)

        self.assertEqual(settings.access_token_string, None)

    def test_Settings_save_load(self):

        # pre-load Settings with a different test
        self.test_Settings_access_token()

        settings = Settings(Test3._app_id)

        self.assertEqual(settings.access_token_string, Test3._access_token)
        self.assertEqual(settings.service_root, Test3._service_root)


if __name__ == '__main__':
    unittest.main()
