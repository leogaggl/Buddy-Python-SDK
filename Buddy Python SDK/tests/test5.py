import unittest

import Buddy
import TestBase

class Test_test5(TestBase.TestBase):
    def test_put_metrics(self):
        Buddy.Buddy.init(TestBase.TestBase.US_app_id, TestBase.TestBase.US_app_key)

        Buddy.Buddy.post("/metrics/events/key", {})

if __name__ == '__main__':
    unittest.main()
