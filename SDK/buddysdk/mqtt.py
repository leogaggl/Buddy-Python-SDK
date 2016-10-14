import sys
import base64
if sys.version_info.major < 3:
    from flufl.enum import IntEnum
else:
    from enum import IntEnum
    basestring = str
import events as events_package
import paho.mqtt.client as mqtt
if sys.version_info.major < 3:
    from urlparse import urlparse
else:
    from urllib.parse import urlparse

import buddy
from settings import Settings
from buddy_events import BuddyEvents
import https


class RootLevels(IntEnum):
    cmd = 1
    status = 2
    telemetry = 3


class Topic(object):

    def __init__(self, root_level, levels):
        self._root_level = root_level
        self._levels = levels

    def __repr__(self):
        return self._root_level.name + "/" + str.join("/", self._levels)

    @classmethod
    def create(cls, root_level, levels=None):
        parsed_root_level = None
        parsed_levels = None;

        if isinstance(root_level, basestring):
            split_levels = root_level.split("/")

            parsed_root_level = [[rl.name is l for rl in iter(RootLevels)] for l in split_levels]
        else:
            if root_level in list(RootLevels):
                parsed_root_level = root_level

        if isinstance(levels, basestring):
            parsed_levels = levels.split("/")
        else:
            if isinstance(levels, list):
                parsed_levels = levels

        if parsed_root_level is None or parsed_levels is None:
            return None
        else:
            return cls(parsed_root_level, parsed_levels)

    @property
    def root_level(self):
        return self._root_level

    @property
    def levels(self):
        return self._levels


class Qos(IntEnum):
    at_most_once = 0
    at_least_once = 1


class MqttEvents(object):

    def __init__(self):
        self._published = events_package.Events()
        self._publish_received = events_package.Events()

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

        buddy.https_client = https.Https(buddy.events, buddy.settings)

        buddy.mqtt_client = MqttEvents()

        buddy.mqtt_client = cls(buddy.events, buddy.mqtt_client, buddy.settings, buddy.https_client)

        return buddy.mqtt_client

    def __on_disconnect(self, client, userdata, rc):
        self._events.connection_changed.on_change(userdata, rc)

    def __on_message(self, client, userdata, msg):
        self._mqtt_events.publish_received.on_change(userdata, msg)

    def __on_publish(self, client, userdata, mid):
        self._mqtt_events.published.on_change(userdata, mid)

    def __on_debug_connect(self, client, userdata, flags, rc):
        print(userdata)

    def __on_debug_log(self, client, userdata, level, buf):
        print(buf)

    def connect(self):
        access_token = self._https.get_access_token_string()

        if access_token is None or access_token is "":
            self._events.service_exception.on_change()
        else:
            self._client = mqtt.Client(client_id=access_token)

            self._client.on_disconnect = self.__on_disconnect
            self._client.on_message = self.__on_message
            self._client.on_publish = self.__on_publish
            self._client.on_connect = self.__on_debug_connect
            self._client.on_log = self.__on_debug_log

            try:
                self._client.connect("co-us.buddyplatform.com", 8883)

                self._client.loop_start()

                global_topic = Topic.create(RootLevels.cmd, "#")
                self._client.subscribe(str(global_topic))

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

    def publish(self, topic, payload, qos=Qos.at_most_once):
        try:
            if topic.root_level is not RootLevels.telemetry:
                payload = base64.standard_b64encode(payload.encode('ascii'))

            result = self._client.publish(str(topic), payload, int(qos))
            return result
        except BaseException as ex:
            self._events.service_exception.on_change(ex)
            return ex
