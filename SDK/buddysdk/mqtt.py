import paho.mqtt.client as mqtt
import paho.mqtt.publish
import paho.mqtt.subscribe
from enum import Enum
import events
import requests
import sys
from threading import Thread
from urlparse import urlparse
import uuid

import buddy
from settings import Settings
from buddy_events import BuddyEvents
from https import Https


class RootLevels(Enum):
    cmd = "cmd"
    status = "status"
    telemetry = "telemetry"


class Topic(object):

    def __init__(self, root_level, levels):
        self._root_level = root_level
        self._levels = levels

    @classmethod
    def from_string(cls, levels):
        obj = cls()
        obj._levels = levels
        return obj

    @property
    def root_level(self):
        return self._root_level

    @property
    def levels(self):
        return self._levels


class Qos(Enum):
    at_most_once = 0,
    at_least_once = 1


class MqttEvents(object):

    def __init__(self):
        self._published = events.Events()
        self._publish_received = events.Events()

    @property
    def published(self):
        return self._published

    @property
    def publish_received(self):
        return self._publish_received


class Mqtt(object):
    def __init__(self, events, mqtt_events, settings, https):
        self._events = events
        self._mqtt_events = mqtt_events
        self._https = https
        self._settings = settings
        self._client = None

    @classmethod
    def init(cls, app_id, app_key):
        buddy.events = BuddyEvents()

        buddy.settings = Settings(app_id, app_key)

        buddy.https_client = Https(buddy.events, buddy.settings)

        buddy.mqtt_client = MqttEvents()

        buddy.mqtt_client = cls(buddy.events, buddy.mqtt_client, buddy.settings, buddy.https_client)

        return buddy.mqtt_client

    def __on_disconnect(self, client, userdata, rc):
        self._events.connection_changed.on_change(userdata, rc)

    def __on_message(self, client, userdata, msg):
        self._mqtt_events.publish_received.on_change(userdata, msg)

    def __on_publish(self, client, userdata, mid):
        self._mqtt_events.published.on_change(userdata, mid)

    def connect(self):
        access_token = self._https.get_access_token_string()

        if access_token is None or access_token is "":
            self._events.service_exception.on_change()
        else:
            self._client = mqtt.Client(access_token)

            self._client.on_disconnect = self.__on_disconnect
            self._client.on_message = self.__on_message
            self._client.on_publish = self.__on_publish

            try:
                # TODO: remove when TLS is working for MQTT
                self._client.tls_insecure_set(True)

                self._client.connect(self.url, 1883)

                self._client.loop_start()
            except BaseException as ex:
                self._events.service_exception.on_change(ex)
            else:
                return self._client

    @property
    def events(self):
        return self._events

    @property
    def mqtt_events(self):
        return self._mqtt_events

    @property
    def url(self):
        root = self._settings.service_root

        url = urlparse(root)

        return url.netloc

    def disconnect(self):
        self._client.on_disconnect = None
        self._client.on_message = None
        self._client.on_publish = None

        self._client.disconnect()

        self._client = None

    def publish(self, topic, payload, qos=Qos.at_least_once):
        try:
            self._client.publish(topic, payload, qos)
        except BaseException as ex:
            self._events.service_exception.on_change(ex)
