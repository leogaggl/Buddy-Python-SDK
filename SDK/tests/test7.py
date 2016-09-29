import mock
import time
import unittest

import buddy
from settings import Settings
from test_base import TestBase


class Test7(TestBase):

    @mock.patch('https.Settings')
    def test_create_user(self, settings_mock):
        settings_mock.return_value = Settings(TestBase.US_app_id, TestBase.US_app_key)

        self.setup_with_bad_tokens(settings_mock.return_value)

        buddy.https(TestBase.US_app_id, TestBase.US_app_key)

        users = buddy.https.get("/users", {})
        self.assertIsNotNone(users)

        device_token = settings_mock.return_value.access_token_string
        self.assertIsNotNone(device_token)

        user_response = self.create_test_user()
        self.assertIsNotNone(user_response)

        user_token = settings_mock.return_value.access_token_string
        self.assertIsNotNone(user_token)

        self.assertNotEqual(device_token, user_token)

        self.assertEqual(buddy.current_user_id, user_response["result"]["id"])

    @mock.patch('https.Settings')
    def test_create_logout_login_user(self, settings_mock):
        settings_mock.return_value = Settings(TestBase.US_app_id, TestBase.US_app_key)

        self.setup_with_bad_tokens(settings_mock.return_value)

        buddy.https(TestBase.US_app_id, TestBase.US_app_key)

        users_response = buddy.https.get("/users", {})
        self.assertIsNotNone(users_response)

        device_token = settings_mock.return_value.access_token_string
        self.assertIsNotNone(device_token)

        user_name = self.get_test_user_name()
        user1_response = self.create_test_user(user_name)
        self.assertIsNotNone(user1_response)

        user_token = settings_mock.return_value.access_token_string
        self.assertIsNotNone(user_token)

        buddy.https.logout_user()

        device_token_2 = settings_mock.return_value.access_token_string

        self.assertEqual(device_token, device_token_2)
        self.assertNotEqual(device_token, user_token)
        self.assertNotEqual(device_token_2, user_token)

        user2_response = buddy.https.login_user(user_name, self.get_test_user_password())
        self.assertIsNotNone(user2_response)

        self.assertEqual(user1_response["result"]["id"], user2_response["result"]["id"])
        self.assertEqual(buddy.current_user_id, user2_response["result"]["id"])

    def test_upload_pic(self):
        buddy.https(TestBase.US_app_id, TestBase.US_app_key)

        self.create_test_user()

        # TODO: to run in Python Tools for VS, change to "tests\Buddy Logo.png"
        response = buddy.https.post("/pictures", {}, file=(open("Buddy Logo.png", "rb"), "image/png"))
        self.assertIsNotNone(response)
        self.assertIsNotNone(response["result"]["signedUrl"])

    @mock.patch('https.Settings')
    def test_auth_error(self, settings_mock):
        settings_mock.return_value = Settings(TestBase.US_app_id, TestBase.US_app_key)
        self.setup_with_bad_tokens(settings_mock.return_value)

        buddy.https(TestBase.US_app_id, TestBase.US_app_key,)

        response = buddy.https.get("/pictures", {})
        self.assertIsNotNone(response)
        self.assertEqual(response["status"], 403)

    def test_auth(self):
        buddy.https(TestBase.US_app_id, TestBase.US_app_key)

        logger = AuthLogger()

        self.create_test_user()

        buddy.https.logout_user()

        buddy.user_authentication_needed.on_change += logger.log

        response = buddy.https.get("/pictures", {})
        self.assertIsNotNone(response)

        while logger.authorize_needed is not True:
            time.sleep(2)

    def test_last_location(self):
        buddy.https(TestBase.US_app_id, TestBase.US_app_key)

        self.create_test_user()

        location = (42.0, -42.0)
        buddy.last_location = location

        response = buddy.https.post("/checkins", {})
        self.assertIsNotNone(response)
        result = response["result"]
        self.assertIsNotNone(result)

        response = buddy.https.get("/checkins/" + result["id"], {})
        self.assertIsNotNone(response)
        result = response["result"]
        self.assertIsNotNone(result)
        self.assertEqual(result["location"], {u'lat': location[0], u'lng': location[1]})


class AuthLogger(object):
    def __init__(self):
        self.authorize_needed = False

    def log(self):
        self.authorize_needed = True


if __name__ == '__main__':
    unittest.main()
