import logging
import unittest

import buddy
from .test_base import TestBase


class Test5(TestBase):
    def test_put_metrics(self):
        buddy.init(TestBase.US_app_id, TestBase.US_app_key, "test_put_metrics")

        response = buddy.post("/metrics/events/key", {})

        self.assertIsNotNone(response)

    # TODO: run with network off, switch logic in assertion
    def test_service_exception(self):
        buddy.init(TestBase.US_app_id, TestBase.US_app_key, "test_service_exception")

        logger = ExceptionLogger()

        buddy.service_exception.on_change += logger.log

        response = buddy.post("/metrics/events/key", {})
        self.assertIsNone(response["exception"])


class ExceptionLogger(object):
    def log(self, exception):
        logging.info("service_exception.log: " + str(exception))


if __name__ == '__main__':
    unittest.main()
