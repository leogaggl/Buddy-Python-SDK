import mock
import time

import buddy
from test_base import TestBase


class Test8(TestBase):

    def test_connect(self):
        buddy.init_mqtt(TestBase.US_app_id, TestBase.US_app_key)

        client = buddy.mqtt.connect()

        self.assertIsNotNone(client)

    def test_connect_2(self):
        buddy.init_mqtt(TestBase.US_app_id, TestBase.US_app_key)

        client = buddy.mqtt.connect()

        logger = PublishReceivedLogger()

        buddy.mqtt.mqtt_events.publish_received.on_change += logger.log

        self.assertIsNotNone(client)

        while logger.publish_received is not True:
            time.sleep(2)


class PublishReceivedLogger(object):
    def __init__(self):
        self.publish_received = False

    def log(self, client, userdata, msg):
        self.publish_received = True
