import datetime
import easysettings
import re
import requests

class Settings(object):

    _service_root = None
    _device_token = None
    _device_token_expires = None
    _default_service_root = "https://api.buddyplatform.com"


    def __init__(self, app_id):
        self._settings = easysettings.EasySettings("buddy.conf", app_id)
        self._service_root = self._settings.get("service_root")
        self._device_token = self._settings.get("device_token")

    @property
    def service_root(self):
        if self._service_root == "":
            return self._default_service_root

        return self._service_root

    @property
    def access_token(self):
        if self._device_token != "" and self._device_token_expires > datetime.datetime.now():
            return self._device_token
        else:
            return ""

    def process_device_registration(self, response):
        self._device_token = response["accessToken"]
        self._device_token_expires = self.get_ticks(response["accessTokenExpires"])
        
        if ("serviceRoot" in response):
            self._service_root = response["serviceRoot"]

        self._settings.save()

    def get_ticks(self, javascript_ticks):
        match = re.compile("\/Date\((\d+)\)\/").findall(javascript_ticks)[0]

        ticks = datetime.datetime.utcfromtimestamp(int(match)/1000)

        return ticks
