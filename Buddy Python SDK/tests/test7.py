import unittest
from uuid import uuid4

from buddy import Buddy
from settings import Settings
from test_base import TestBase


class Test_test7(TestBase):

    def test_create_user(self):
        self.setup_with_bad_device_token()

        Buddy.init(TestBase.US_app_id, TestBase.US_app_key)

        users = Buddy.get("/users")
        self.assertIsNotNone(users)

        settings = Settings(TestBase.US_app_id)
        device_token = settings.access_token_string
        self.assertIsNotNone(device_token)

        user = Buddy.create_user("testuser" + str(uuid4()), "testpassword")
        self.assertIsNotNone(user)

        settings = Settings(TestBase.US_app_id)
        user_token = settings.access_token_string
        self.assertIsNotNone(user_token)

        self.assertNotEqual(device_token, user_token)

        self.assertEqual(Buddy.current_user_id, user["id"])

    def test_create_logout_login_user(self):
        self.setup_with_bad_device_token()

        Buddy.init(TestBase.US_app_id, TestBase.US_app_key)

        users = Buddy.get("/users")
        self.assertIsNotNone(users)

        settings = Settings(TestBase.US_app_id)
        device_token = settings.access_token_string

        testuser = "testuser" + str(uuid4())
        testpassword = "testpassword"
        user1 = Buddy.create_user(testuser, testpassword)
        self.assertIsNotNone(user1)

        settings = Settings(TestBase.US_app_id)
        user_token = settings.access_token_string

        Buddy.logout_user()

        settings = Settings(TestBase.US_app_id)
        device_token_2 = settings.access_token_string

        self.assertEqual(device_token, device_token_2)
        self.assertNotEqual(device_token, user_token)
        self.assertNotEqual(device_token_2, user_token)

        user2 = Buddy.login_user(testuser, testpassword)
        self.assertIsNotNone(user2)

        self.assertEqual(user1["id"], user2["id"])
        self.assertEqual(Buddy.current_user_id, user2["id"])


if __name__ == '__main__':
    unittest.main()
