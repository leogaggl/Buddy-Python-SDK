import mprop

from buddy_events import BuddyEvents
from https import Https
from mqtt import Mqtt, MqttEvents
from settings import Settings


__https_client = None
__mqtt_client = None
__settings = None
__events = None
__mqtt_events = None


@property
def https(module):
    return __https_client


@property
def mqtt(module):
    return __mqtt_client


@property
def app_id(module):
    return __settings.app_id


@property
def current_user_id(module):
    return __https_client.current_user_id


@property
def last_location(module):
    return __settings.last_location


@last_location.setter
def last_location(module, value):
    __settings.last_location = value


@property
def service_exception(module):
    return __events.service_exception


@property
def connection_changed(module):
    return __events.connection_changed


@property
def user_authentication_needed(module):
    return __events.user_authentication_needed


@property
def connection_changed(module):
    return __events.connection_changed


@property
def user_authentication_needed(module):
    return __events.user_authentication_needed


def init_https(module, app_id, app_key):
    global __events, __https_client, __settings

    __events = BuddyEvents()

    __settings = Settings(app_id, app_key)

    __https_client = Https(__events, __settings)

    return __https_client


def init_mqtt(module, app_id, app_key):
    global __mqtt_client, __https_client

    module.init_https(app_id, app_key)

    __mqtt_client = MqttEvents()

    __mqtt_client = Mqtt(__events, __mqtt_client, __settings, __https_client)

    return __mqtt_client

mprop.init()
