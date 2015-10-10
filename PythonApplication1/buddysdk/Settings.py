import datetime
import easysettings


class Settings(object):

    _service_root = None
    _device_token = None
    _device_token_expires = None
    _default_service_root = "https://api.buddyplatform.com/"


    def __init__(self, app_id):
        self._settings = easysettings.EasySettings("buddy.conf", app_id)
        self._service_root = self._settings.get("service_root")
        self._device_token = self._settings.get("device_token")

    def get_service_root(self):
        if self._service_root == None:
            return self._default_service_root

        return self._service_root

    def get_access_token(self):
        if self._device_token != None and self._device_token_expires > datetime.datetime.now():
            return self._device_token
        else:
            return None

    def process_device_registration(self, response):
        self._device_token = response[0]["accessToken"]
        self._device_token_expires = datetime.datetime.utcfromtimestamp(int(response[0]["accessTokenExpires"])/1000)
        self._service_root = response[0]["serviceRoot"]

        self._settings.save()
