import json
import time
import unittest

import buddy
import mqtt
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

    def test_send_mqtt_telemetry(self):
        buddy.mqtt(TestBase.US_app_id, TestBase.US_app_key)

        client = buddy.mqtt.connect()

        self.assertIsNotNone(client)

        telemetry_topic = mqtt.Topic.create(mqtt.RootLevels.telemetry, "telemetry_config")

        payload = json.dumps({"data": {"value": 1}})

        message_info = buddy.mqtt.publish(telemetry_topic, payload)

        self.assertIsNotNone(message_info)


class PublishReceivedLogger(object):
    def __init__(self):
        self.publish_received = False

    def log(self, userdata, msg):
        print(msg)
        self.publish_received = True


if __name__ == '__main__':
    unittest.main()
