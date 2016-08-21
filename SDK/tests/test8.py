import mock
import time

import buddy
from settings import Settings
from test_base import TestBase


class Mqtt(TestBase):

    def test_connect(self):
        x = 3