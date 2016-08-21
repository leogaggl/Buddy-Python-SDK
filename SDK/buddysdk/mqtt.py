import paho.mqtt.client as mqtt
import paho.mqtt.publish
import paho.mqtt.subscribe
from enum import Enum
import platform
import requests
import sys
from threading import Thread
import uuid

from buddy_events import BuddyEvents
from connection import Connection
from https import Https
from settings import Settings


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



class Mqtt(object):
    def __init__(self, events, settings, https):
        self._https = https
        self._client = mqtt.Client()
        self._client.on_disconnect = self.__on_disconnect
        self._client.on_message = self.__on_message
        self._client.on_publish = self.__on_publish
        self._connection_closed = Events()
        self._published = Events()
        self._publish_received = Events()

    @property
    def connection_closed(self):
        return self._connection_closed

    @property
    def published(self):
        return self._published

    @property
    def publish_received(self):
        return self._publish_received

    def __on_disconnect(self, client, userdata, rc):
        self._connection_closed.on_change(userdata, rc)

    # The callback for when a PUBLISH message is received from the server.
    def __on_message(self, client, userdata, msg):
        self._publish_received.on_change(userdata, msg)

    # The callback for when a PUBLISH message is received from the server.
    def __on_publish(self, client, userdata, mid):
        self._published.on_change(userdata, mid)

    def connect(self):
        x = ""
        self._client.connect('api.buddyplatform.com', 1883)
        self._client.loop_start()
