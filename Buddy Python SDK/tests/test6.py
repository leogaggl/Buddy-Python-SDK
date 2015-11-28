import unittest
import logging
import time

from buddy import Buddy
from connection import Connection
from test_base import TestBase
from settings import Settings


class Test_test6(TestBase):

    def test_connection(self):
        Buddy.init(TestBase.US_app_id, TestBase.US_app_key)

        logger = ConnectionLogger();

        Buddy.connection_changed.on_change += logger.log

        Buddy.post("/metrics/events/key", {})

        while logger.connection is not Connection.On:
            time.sleep(2)

    def test_bad_device_token(self):
        settings = Settings(TestBase.US_app_id)
        settings._settings.set(Settings._device_token, ["bad device token", self.future_javascript_access_token_expires()])

        client = Buddy.init(TestBase.US_app_id, TestBase.US_app_key)

        Buddy.post("/metrics/events/key", {})

        self.assertIsNotNone(client.get_access_token_string())

    def test_device_token_expired(self):
        settings = Settings(TestBase.US_app_id)
        settings._settings.set(Settings._device_token, ["eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOiIyMDE1LTExLTExVDAzOjM0OjU4LjE2Mjg2NzlaIiwibCI6ImJiYmJ2LnJwZGJ2eGJnR3JNZyIsImEiOiJiYmJiYmMueGdqYnZQZHdrbGx3IiwidSI6bnVsbCwiZCI6ImJsai5sRHBGd0tNc2dGRk0ifQ.l4ob5liSYfgI25mnysjRHpgCYr1yCzayC4XjHJOv4v0",
                                                        self.past_javascript_access_token_expires()])

        client = Buddy.init(TestBase.US_app_id, TestBase.US_app_key)

        Buddy.post("/metrics/events/key", {})

        self.assertIsNotNone(client.get_access_token_string())


class ConnectionLogger(object):
    def __init__(self):
        self.connection = Connection.On # switch to None when debugging w\ no connection

    def log(self, connection):
        logging.info("connectivity_logger: " + str(connection.value))
        self.connection = connection


if __name__ == '__main__':
    unittest.main()
