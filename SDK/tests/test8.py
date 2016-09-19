import time
import unittest

import buddy
from test_base import TestBase


class Test8(TestBase):

    def test_connect(self):
        buddy.init(TestBase.US_app_id, TestBase.US_app_key)

        client = buddy.mqtt.connect()

        self.assertIsNotNone(client)

    @unittest.skip("Command must be sent to the server manually")
    def test_publish_received(self):
        buddy.mqtt(TestBase.US_app_id, TestBase.US_app_key)

        client = buddy.mqtt.connect()

        logger = PublishReceivedLogger()

        buddy.mqtt.mqtt_events.publish_received.on_change += logger.log

        self.assertIsNotNone(client)

        while logger.publish_received is not True:
            time.sleep(2)


class PublishReceivedLogger(object):
    def __init__(self):
        self.publish_received = False

    def log(self, userdata, msg):
        print(msg)
        self.publish_received = True


if __name__ == '__main__':
    unittest.main()
