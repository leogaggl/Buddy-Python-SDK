import configparser
import re
from access_token import AccessToken

class Settings(object):
    _service_root = "service_root"
    _device_token = "device"
    _user_token = "user"
    _user_id = "user_id"
    _default_service_root = "https://api.buddyplatform.com"

    def __init__(self, app_id):
        self._app_id = app_id

        self._settings = configparser.ConfigParser()
        self._settings.read("buddy.cfg")

        if not self._settings.has_section(self._app_id):
            self._settings.add_section(self._app_id)

    @property
    def service_root(self):
        service_root = self.__get(Settings._service_root)
        if service_root is None:
            return Settings._default_service_root
        else:
            return service_root

    @property
    def access_token_string(self):
        if self.user_token.token is not None:
            return self.user_token.token
        elif self.device_token.token is not None:
            return self.device_token.token

    @property
    def device_token(self):
        return AccessToken(self.__get_access_token(Settings._device_token))

    def set_device_token(self, response):
        self.__set_access_token(Settings._device_token, response)

        if response is None or "serviceRoot" not in response:
            self.__remove(Settings._service_root)
        else:
            self.__set(Settings._service_root, response["serviceRoot"])

        self.__save()

    def __set_access_token(self, settings_token_key, response):
        if response is None:
            self.__remove(settings_token_key + "_access_token")
            self.__remove(settings_token_key + "_access_token_expires")
        else:
            self.__set(settings_token_key + "_access_token", response["accessToken"])
            self.__set(settings_token_key + "_access_token_expires",
                       self.__ticks_from_javascript_datetime(response["accessTokenExpires"]))

    def __get_access_token(self, settings_token_key):
        return [self.__get(settings_token_key + "_access_token"),
                           self.__get(settings_token_key + "_access_token_expires")]

    def __ticks_from_javascript_datetime(self, javascript_datetime):
        return re.compile("\/Date\((\d+)\)\/").findall(javascript_datetime)[0]

    @property
    def user_token(self):
        return AccessToken(self.__get_access_token(Settings._user_token))

    @property
    def user_id(self):
        return self.__get(Settings._user_id)

    def set_user(self, response):
        self.__set_access_token(Settings._user_token, response)

        if response is None:
            self.__remove(Settings._user_id)
        else:
            self.__set(Settings._user_id, response["id"])

        self.__save()

    def __save(self):
        with open('buddy.cfg', 'w+') as configfile:
            self._settings.write(configfile)

    def __get(self, option):
        if self._settings.has_option(self._app_id, option):
            return self._settings.get(self._app_id, option)
        else:
            return None

    def __set(self, option, value):
        return self._settings.set(self._app_id, option, value)

    def __remove(self, option):
        return self._settings.remove_option(self._app_id, option)