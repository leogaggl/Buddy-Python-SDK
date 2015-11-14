import unittest
import logging
import time

import Buddy
import TestBase
from Connection import Connection


class Test_test6(TestBase.TestBase):
    def test_connection(self):
        Buddy.Buddy.init(TestBase.TestBase.US_app_id, TestBase.TestBase.US_app_key)

        logger = connection_logger();

        Buddy.Buddy.connection_changed.on_change += logger.log

        Buddy.Buddy.post("/metrics/events/key", {})

        while logger.connection is not Connection.On:
            time.sleep(2)


class connection_logger(object):
    def __init__(self):
        self.connection = Connection.On # switch to None when debugging w\ no connection

    def log(self, connection):
        logging.info("connectivity_logger: " + str(connection.value))
        self.connection = connection


if __name__ == '__main__':
    unittest.main()
