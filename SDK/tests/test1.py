import unittest

from https import Https
from .test_base import TestBase


class Test1(TestBase):

    def test_Https(self):
        client = Https(TestBase.US_app_id, TestBase.US_app_key)
        self.assertIsNotNone(client)
        self.assertIs(client.app_id, TestBase.US_app_id)
        self.assertIs(client.app_key, TestBase.US_app_key)


if __name__ == '__main__':
    unittest.main()
