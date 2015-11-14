import unittest

from Buddy import Buddy
from TestBase import TestBase

class Test_test5(TestBase):
    def test_put_metrics(self):
        Buddy.init(TestBase.US_app_id, TestBase.US_app_key)

        Buddy.post("/metrics/events/key", {})

if __name__ == '__main__':
    unittest.main()
