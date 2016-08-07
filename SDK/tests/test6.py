import logging
import time
import unittest

import buddy
from connection import Connection
from settings import Settings
from .test_base import TestBase


class Test6(TestBase):

    # TODO: run with network off and a breakpoint at time.sleep
    def test_connection(self):
        buddy.init(TestBase.US_app_id, TestBase.US_app_key, "test_connection")

        logger = ConnectionLogger()

        buddy.connection_changed.on_change += logger.log

        buddy.post("/metrics/events/key", {})

        while logger.connection is not Connection.on:
            time.sleep(2)

    def test_bad_device_token(self):
        settings = Settings(TestBase.US_app_id)
        settings.set_device_token({"accessToken": "bad device token",
                                   "accessTokenExpires": self.future_javascript_access_token_expires()})

        client = buddy.init(TestBase.US_app_id, TestBase.US_app_key, "test_bad_device_token")

        buddy.post("/metrics/events/key", {})

        self.assertIsNotNone(client.get_access_token_string())

    def test_device_token_expired(self):
        settings = Settings(TestBase.US_app_id)
        settings.set_device_token({"accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOiIyMDE1LTExLTExVDAzOjM0OjU4LjE2Mjg2NzlaIiwibCI6ImJiYmJ2LnJwZGJ2eGJnR3JNZyIsImEiOiJiYmJiYmMueGdqYnZQZHdrbGx3IiwidSI6bnVsbCwiZCI6ImJsai5sRHBGd0tNc2dGRk0ifQ.l4ob5liSYfgI25mnysjRHpgCYr1yCzayC4XjHJOv4v0",
                                   "accessTokenExpires": self.past_javascript_access_token_expires()})

        client = buddy.init(TestBase.US_app_id, TestBase.US_app_key, "test_device_token_expired")

        buddy.post("/metrics/events/key", {})

        self.assertIsNotNone(client.get_access_token_string())


class ConnectionLogger(object):
    def __init__(self):
        self.connection = Connection.on # TODO: switch to None when debugging test_connection

    def log(self, connection):
        logging.info("connection_changed.log: " + str(connection.value))
        self.connection = connection


if __name__ == '__main__':
    unittest.main()
