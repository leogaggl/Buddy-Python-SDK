from easysettings import EasySettings
import re
from access_token import AccessToken


class Settings(object):
    _service_root = "service_root"
    _device_token = "device_token"
    _user_token = "user_token"
    _default_service_root = "https://api.buddyplatform.com"

    def __init__(self, app_id):
        self._settings = EasySettings("buddy.conf", app_id)

    @property
    def service_root(self):
        service_root = self._settings.get(Settings._service_root)
        if service_root is "":
            return Settings._default_service_root
        else:
            return service_root

    @property
    def access_token_string(self):
        if self.__user_token.token:
            return self.__user_token.token
        elif self.__device_token.token:
            return self.__device_token.token

        return None

    @property
    def __device_token(self):
        return AccessToken(self._settings.get(Settings._device_token))

    def set_device_token(self, response):
        if response is not None:
            self.__set_access_token(Settings._device_token, response)

            if "serviceRoot" in response:
                self._settings.set(Settings._service_root, response["serviceRoot"])

            self._settings.save()
   
    def __set_access_token(self, settings_token_key, response):
        if response is None:
            self._settings.remove(settings_token_key)
        else:
            self._settings.set(settings_token_key,
                [response["accessToken"], self.__ticks_from_javascript_datetime(response["accessTokenExpires"])])

    def __ticks_from_javascript_datetime(self, javascript_datetime):
        return re.compile("\/Date\((\d+)\)\/").findall(javascript_datetime)[0]

    @property
    def __user_token(self):
        return AccessToken(self._settings.get(Settings._user_token))

    def set_user_token(self, response):
        if response is not None:
            self.__set_access_token(Settings._user_token, response)

            self._settings.save()