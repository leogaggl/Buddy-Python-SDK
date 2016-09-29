import logging
import time
import unittest

import buddy
from connection import Connection
from settings import Settings
from test_base import TestBase


class Test6(TestBase):

    # When debugging run with network off and a breakpoint at time.sleep
    def test_connection(self):
        buddy.https(TestBase.US_app_id, TestBase.US_app_key)

        logger = ConnectionLogger()

        buddy.connection_changed.on_change += logger.log

        while logger.connection is not Connection.on:
            print ("post")
            print(str(buddy.https.post("/metrics/events/key", {})))
            print ("sleep")
            time.sleep(10)

    def test_bad_device_token(self):
        settings = Settings(TestBase.US_app_id, TestBase.US_app_key)
        settings.set_device_token({"accessToken": "bad device token",
                                   "accessTokenExpires": self.future_javascript_access_token_expires()})

        client = buddy.https(TestBase.US_app_id, TestBase.US_app_key)

        buddy.https.post("/metrics/events/key", {})

        self.assertIsNotNone(client.get_access_token_string())

    def test_device_token_expired(self):
        settings = Settings(TestBase.US_app_id, TestBase.US_app_key)
        settings.set_device_token({"accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOiIyMDE1LTExLTExVDAzOjM0OjU4LjE2Mjg2NzlaIiwibCI6ImJiYmJ2LnJwZGJ2eGJnR3JNZyIsImEiOiJiYmJiYmMueGdqYnZQZHdrbGx3IiwidSI6bnVsbCwiZCI6ImJsai5sRHBGd0tNc2dGRk0ifQ.l4ob5liSYfgI25mnysjRHpgCYr1yCzayC4XjHJOv4v0",
                                   "accessTokenExpires": self.past_javascript_access_token_expires()})

        client = buddy.https(TestBase.US_app_id, TestBase.US_app_key)

        buddy.https.post("/metrics/events/key", {})

        self.assertIsNotNone(client.get_access_token_string())


class ConnectionLogger(object):
    def __init__(self):
        print("connection_changed.log start")
        self.connection = Connection.on  # When debugging test_connection switch to None

    def log(self, connection):
        print("connection_changed.log: " + str(connection.value))
        self.connection = connection


if __name__ == '__main__':
    unittest.main()
