import unittest
import logging
import time

from Buddy import Buddy
from TestBase import TestBase
from Connection import Connection


class Test_test6(TestBase):
    def test_connection(self):
        Buddy.init(TestBase.US_app_id, TestBase.US_app_key)

        logger = connection_logger();

        Buddy.connection_changed.on_change += logger.log

        Buddy.post("/metrics/events/key", {})

        while logger.connection is not Connection.On:
            time.sleep(2)

    def test_bad_device_token(self):
        Buddy.init(TestBase.US_app_id, TestBase.US_app_key)

        Buddy.post("/metrics/events/key", {})


class connection_logger(object):
    def __init__(self):
        self.connection = Connection.On # switch to None when debugging w\ no connection

    def log(self, connection):
        logging.info("connectivity_logger: " + str(connection.value))
        self.connection = connection


if __name__ == '__main__':
    unittest.main()
