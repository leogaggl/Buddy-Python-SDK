import mprop
import https as https_module
import mqtt as mqtt_module


https_client = None
mqtt_client = None
settings = None
events = None
mqtt_events = None


@property
def https(module):
    return https_module.Https.init if https_client is None else https_client


@property
def mqtt(module):
    return mqtt_module.Mqtt.init if mqtt_client is None else mqtt_client


@property
def app_id(module):
    return settings.app_id


@property
def current_user_id(module):
    return https_client.current_user_id


@property
def last_location(module):
    return settings.last_location


@last_location.setter
def last_location(module, value):
    settings.last_location = value


@property
def service_exception(module):
    return events.service_exception


@property
def connection_changed(module):
    return events.connection_changed


@property
def user_authentication_needed(module):
    return events.user_authentication_needed


@property
def connection_changed(module):
    return events.connection_changed

@property
def user_authentication_needed(module):
    return events.user_authentication_needed


mprop.init()
