import configparser
import re
import os
import uuid

from access_token import AccessToken


class Settings(object):
    buddy_cfg_name = "buddy.cfg"
    _service_root_name = "service_root"
    _device_token_name = "device"
    _user_token_name = "user"
    _user_id_name = "user_id"
    _unique_id_name = "unique_id"
    _default_service_root = "https://api.buddyplatform.com"
    _access_token_name_suffix = "_access_token"
    _access_token_expires_name_suffix = "_access_token_expires"

    def __init__(self, app_id):
        self._app_id = app_id

        self._settings = configparser.ConfigParser()
        if os.path.isfile(Settings.buddy_cfg_name):
            with open(Settings.buddy_cfg_name, "r") as configfile:
                self._settings.read_file(configfile)

        if not self._settings.has_section(self._app_id):
            self._settings.add_section(self._app_id)

    @property
    def service_root(self):
        service_root = self.__get(Settings._service_root_name)
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
        return AccessToken(self.__get_access_token(Settings._device_token_name))

    def set_device_token(self, response):
        self.__set_access_token(Settings._device_token_name, response)

        if response is None or "serviceRoot" not in response:
            self.__remove(Settings._service_root_name)
        else:
            self.__set(Settings._service_root_name, response["serviceRoot"])

        self.__save()

    def __get_access_token(self, settings_token_name):
        return [self.__get(settings_token_name + Settings._access_token_name_suffix),
                self.__get(settings_token_name + Settings._access_token_expires_name_suffix)]

    def __set_access_token(self, settings_token_name, result):
        if result is None:
            self.__remove(settings_token_name + Settings._access_token_name_suffix)
            self.__remove(settings_token_name + Settings._access_token_expires_name_suffix)
        else:
            self.__set(settings_token_name + Settings._access_token_name_suffix, result["accessToken"])
            self.__set(settings_token_name + Settings._access_token_expires_name_suffix,
                       Settings.__ticks_from_javascript_datetime(result["accessTokenExpires"]))

    @staticmethod
    def __ticks_from_javascript_datetime(javascript_datetime):
        return re.compile("\/Date\((\d+)\)\/").findall(javascript_datetime)[0]

    @property
    def user_token(self):
        return AccessToken(self.__get_access_token(Settings._user_token_name))

    @property
    def user_id(self):
        return self.__get(Settings._user_id_name)

    @property
    def unique_id(self):
        unique_id = self.__get(Settings._unique_id_name)
        if unique_id is None:
            unique_id = str(uuid.getnode())
            self.__set(Settings._unique_id_name, unique_id)
            self.__save()
        return unique_id

    def set_user(self, result):
        self.__set_access_token(Settings._user_token_name, result)

        if result is None:
            self.__remove(Settings._user_id_name)
        else:
            self.__set(Settings._user_id_name, result["id"])

        self.__save()

    def __save(self):
        with open(Settings.buddy_cfg_name, "w") as config_file:
            self._settings.write(config_file)

    def __get(self, option):
        if self._settings.has_option(self._app_id, option):
            return self._settings.get(self._app_id, option)
        else:
            return None

    def __set(self, option, value):
        return self._settings.set(self._app_id, option, value)

    def __remove(self, option):
        return self._settings.remove_option(self._app_id, option)
