import unittest
from uuid import uuid4
import time

from buddy import Buddy
from settings import Settings
from test_base import TestBase
from unittest.mock import patch


class Test_test7(TestBase):

    @patch('buddy_client.Settings')
    def test_create_user(self, settings_mock):
        settings_mock.return_value = Settings(TestBase.US_app_id)

        self.setup_with_bad_tokens(settings_mock.return_value)

        Buddy.init(TestBase.US_app_id, TestBase.US_app_key, "test_create_user")

        users = Buddy.get("/users")
        self.assertIsNotNone(users)

        device_token = settings_mock.return_value.access_token_string
        self.assertIsNotNone(device_token)

        user_response = Buddy.create_user("testuser" + str(uuid4()), "testpassword")
        self.assertIsNotNone(user_response)

        user_token = settings_mock.return_value.access_token_string
        self.assertIsNotNone(user_token)

        self.assertNotEqual(device_token, user_token)

        self.assertEqual(Buddy.current_user_id, user_response["result"]["id"])

    @patch('buddy_client.Settings')
    def test_create_logout_login_user(self, settings_mock):
        settings_mock.return_value = Settings(TestBase.US_app_id)

        self.setup_with_bad_tokens(settings_mock.return_value)

        Buddy.init(TestBase.US_app_id, TestBase.US_app_key, "test_create_logout_login_user")

        users_response = Buddy.get("/users")
        self.assertIsNotNone(users_response)

        device_token = settings_mock.return_value.access_token_string

        test_user = "testuser" + str(uuid4())
        test_password = "testpassword"
        user1_response = Buddy.create_user(test_user, test_password)
        self.assertIsNotNone(user1_response)

        user_token = settings_mock.return_value.access_token_string

        Buddy.logout_user()

        device_token_2 = settings_mock.return_value.access_token_string

        self.assertEqual(device_token, device_token_2)
        self.assertNotEqual(device_token, user_token)
        self.assertNotEqual(device_token_2, user_token)

        user2_response = Buddy.login_user(test_user, test_password)
        self.assertIsNotNone(user2_response)

        self.assertEqual(user1_response["result"]["id"], user2_response["result"]["id"])
        self.assertEqual(Buddy.current_user_id, user2_response["result"]["id"])

    def test_upload_pic(self):
        Buddy.init(TestBase.US_app_id, TestBase.US_app_key, "test_upload_pic")

        test_user = "testuser" + str(uuid4())
        test_password = "testpassword"
        Buddy.create_user(test_user, test_password)

        response = Buddy.post("/pictures", {}, file=(open("Buddy Logo.png", "rb"), "image/png"))
        self.assertIsNotNone(response)
        self.assertIsNotNone(response["result"]["signedUrl"])

    @patch('buddy_client.Settings')
    def test_auth_error(self, settings_mock):
        settings_mock.return_value = Settings(TestBase.US_app_id)
        self.setup_with_bad_tokens(settings_mock.return_value)

        Buddy.init(TestBase.US_app_id, TestBase.US_app_key, "test_auth_error")

        response = Buddy.get("/pictures")
        self.assertIsNotNone(response)
        self.assertEqual(response["status"], 403)

    def test_auth(self):
        Buddy.init(TestBase.US_app_id, TestBase.US_app_key, "test_auth")

        logger = AuthLogger()

        test_user = "testuser" + str(uuid4())
        test_password = "testpassword"
        Buddy.create_user(test_user, test_password)

        Buddy.logout_user()

        Buddy.authentication_needed.on_change += logger.log

        Buddy.get("/pictures", {})

        while logger.authorized is not True:
            time.sleep(2)


class AuthLogger(object):
    def __init__(self):
        self.authorized = False

    def log(self):
        self.authorized = True

if __name__ == '__main__':
    unittest.main()
