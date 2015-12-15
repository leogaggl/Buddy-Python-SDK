import unittest

from buddy import Buddy
from test_base import TestBase


class Test_test5(TestBase):
    def test_put_metrics(self):
        Buddy.init(TestBase.US_app_id, TestBase.US_app_key, "test_put_metrics")

        result = Buddy.post("/metrics/events/key", {})

        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()
