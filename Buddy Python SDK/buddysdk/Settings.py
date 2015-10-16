import datetime
import re

import easysettings


class Settings(object):
    _service_root = "service_root"
    _device_token = "device_token"
    _device_token_expires = "device_token_expires"
    _default_service_root = "https://api.buddyplatform.com"

    def __init__(self, app_id):
        self._settings = easysettings.EasySettings("buddy.conf", app_id)

    @property
    def service_root(self):
        service_root = self._settings.get(Settings._service_root)
        if service_root == "":
            return Settings._default_service_root
        else:
            return service_root

    @property
    def access_token(self):
        device_token = self._settings.get(Settings._device_token)
        if device_token != "" and self.device_token_expires > datetime.datetime.now():
            return device_token
        else:
            return ""

    @property
    def device_token_expires(self):
        device_token_expires_setting = self._settings.get(Settings._device_token_expires)
        if device_token_expires_setting == "":
            return datetime.datetime(0)
        else:
            return datetime.datetime.utcfromtimestamp(int(device_token_expires_setting) / 1000)

    def process_device_registration(self, response):
        self._settings.set(Settings._device_token, response["accessToken"])
        self._settings.set(Settings._device_token_expires, self.ticks_from_javascript_datetime(response["accessTokenExpires"]))
        
        if ("serviceRoot" in response):
            self._settings.set(Settings._service_root, response["serviceRoot"])

        self._settings.save()
   
    def ticks_from_javascript_datetime(self, javascript_datetime):  
        return re.compile("\/Date\((\d+)\)\/").findall(javascript_datetime)[0]