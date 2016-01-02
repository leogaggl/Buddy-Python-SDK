import unittest
from uuid import uuid4

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

        user = Buddy.create_user("testuser" + str(uuid4()), "testpassword")
        self.assertIsNotNone(user)

        user_token = settings_mock.return_value.access_token_string
        self.assertIsNotNone(user_token)

        self.assertNotEqual(device_token, user_token)

        self.assertEqual(Buddy.current_user_id, user["id"])

    @patch('buddy_client.Settings')
    def test_create_logout_login_user(self, settings_mock):
        settings_mock.return_value = Settings(TestBase.US_app_id)

        self.setup_with_bad_tokens(settings_mock.return_value)

        Buddy.init(TestBase.US_app_id, TestBase.US_app_key, "test_create_logout_login_user")

        users = Buddy.get("/users")
        self.assertIsNotNone(users)

        device_token = settings_mock.return_value.access_token_string

        testuser = "testuser" + str(uuid4())
        testpassword = "testpassword"
        user1 = Buddy.create_user(testuser, testpassword)
        self.assertIsNotNone(user1)

        user_token = settings_mock.return_value.access_token_string

        Buddy.logout_user()

        device_token_2 = settings_mock.return_value.access_token_string

        self.assertEqual(device_token, device_token_2)
        self.assertNotEqual(device_token, user_token)
        self.assertNotEqual(device_token_2, user_token)

        user2 = Buddy.login_user(testuser, testpassword)
        self.assertIsNotNone(user2)

        self.assertEqual(user1["id"], user2["id"])
        self.assertEqual(Buddy.current_user_id, user2["id"])

    def test_upload_pic(self):
        Buddy.init(TestBase.US_app_id, TestBase.US_app_key, "test_upload_pic")

        testuser = "testuser" + str(uuid4())
        testpassword = "testpassword"
        Buddy.create_user(testuser, testpassword)

        result = Buddy.post("/pictures", {}, file=(open("Buddy Logo.png", "rb"), "image/png"))
        self.assertIsNotNone(result)
        self.assertIsNotNone(result["signedUrl"])

if __name__ == '__main__':
    unittest.main()
