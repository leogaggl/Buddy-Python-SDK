import mprop

from buddy_events import BuddyEvents
import https as https_module
import mqtt as mqtt_module
from settings import Settings


https_client = None
mqtt_client = None
settings = None
events = None
mqtt_events = None


@property
def https(module):
    return https_module.Https.init if module.https_client is None else module.https_client


@property
def mqtt(module):
    return mqtt_module.Mqtt.init if module.mqtt_client is None else module.mqtt_client


@property
def app_id(module):
    return module.settings.app_id


@property
def current_user_id(module):
    return module.https_client.current_user_id


@property
def last_location(module):
    return module.settings.last_location


@last_location.setter
def last_location(module, value):
    module.settings.last_location = value


@property
def service_exception(module):
    return module.events.service_exception


@property
def connection_changed(module):
    return module.events.connection_changed


@property
def user_authentication_needed(module):
    return module.events.user_authentication_needed


@property
def connection_changed(module):
    return module.events.connection_changed


@property
def user_authentication_needed(module):
    return module.events.user_authentication_needed


def init(module, app_id, app_key):
    # mqtt depends on https, so leverage mqtt's init
    module.mqtt(app_id, app_key)


mprop.init()
