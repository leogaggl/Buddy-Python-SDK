from datetime import datetime
from datetime import timezone
from datetime import timedelta
import unittest

from settings import Settings
from test_base import TestBase
from access_token import AccessToken


class Test_test3(TestBase):

    _app_id = "a"
    _default_service_root = "https://api.buddyplatform.com"
    _service_root = "sr"
    _access_token = "at"

    def test_Settings_empty(self):
        settings = Settings(Test_test3._app_id)
        at = settings.access_token_string
        self.assertEqual(at, None)
        self.assertEqual(settings.service_root, Test_test3._default_service_root)

    def test_access_token(self):
        future = datetime.now(timezone.utc) + timedelta(1)
        at = self.access_token_base(future)
        self.assertEqual(at.token, Test_test3._access_token)

    def test_access_token_expired(self):
        past = datetime.now(timezone.utc) - timedelta(1)
        at = self.access_token_base(past)
        self.assertEqual(at.token, None)

    def access_token_base(self, time):
        at = AccessToken([Test_test3._access_token, str(self.ticks_from_timestamp(time.timestamp()))])
        return at

    def test_Settings_access_token(self):
        settings = Settings(Test_test3._app_id)

        json = {"accessToken": Test_test3._access_token,
                "accessTokenExpires": self.future_javascript_access_token_expires(),
                "serviceRoot": Test_test3._service_root}

        settings.set_device_token(json)

        self.assertEqual(settings.access_token_string, Test_test3._access_token)

    def test_Settings_access_token_expired(self):
        settings = Settings(Test_test3._app_id)

        json = {"accessToken": Test_test3._access_token,
                "accessTokenExpires": self.past_javascript_access_token_expires(),
                "serviceRoot": Test_test3._service_root}

        settings.set_device_token(json)

        self.assertEqual(settings.access_token_string, None)

    def test_Settings_save_load(self):

        # pre-load Settings with a different test
        self.test_Settings_access_token()

        settings = Settings(Test_test3._app_id)

        self.assertEqual(settings.access_token_string, Test_test3._access_token)
        self.assertEqual(settings.service_root, Test_test3._service_root)


if __name__ == '__main__':
    unittest.main()
