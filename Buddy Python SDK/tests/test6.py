import unittest
import logging
import time

import Buddy
import TestBase
import Connection


class Test_test6(TestBase.TestBase):
    def test_connectivity(self):
        Buddy.Buddy.init(TestBase.TestBase.US_app_id, TestBase.TestBase.US_app_key)

        logger = connectivity_logger();

        Buddy.Buddy.connectivity_changed.on_change += logger.log

        Buddy.Buddy.post("/metrics/events/key", {})

        while logger.connectivity is not Connection.Connection.Connection:
            time.sleep(2)


class connectivity_logger(object):
    def __init__(self):
        self.connectivity = Connection.Connection.Connection # switch to None when debugging w\ no connection

    def log(self, connectivity):
        logging.info("connectivity_logger: " + str(connectivity.value))
        self.connectivity = connectivity


if __name__ == '__main__':
    unittest.main()
