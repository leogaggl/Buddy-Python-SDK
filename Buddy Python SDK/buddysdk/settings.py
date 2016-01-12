import configparser
import re
import os
from access_token import AccessToken

class Settings(object):
    _service_root = "service_root"
    _device_token = "device"
    _user_token = "user"
    _user_id = "user_id"
    _default_service_root = "https://api.buddyplatform.com"
    _buddy_cfg = "buddy.cfg"
    _access_token_key = "_access_token"
    _access_token_expires_key = "_access_token_expires"

    def __init__(self, app_id):
        self._app_id = app_id

        self._settings = configparser.ConfigParser()
        if os.path.isfile(Settings._buddy_cfg):
            with open(Settings._buddy_cfg, "r") as configfile:
                self._settings.read_file(configfile)

        if not self._settings.has_section(self._app_id):
            self._settings.add_section(self._app_id)

    @property
    def service_root(self):
        service_root = self._get(Settings._service_root)
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
        return AccessToken(self._get_access_token(Settings._device_token))

    def set_device_token(self, response):
        self._set_access_token(Settings._device_token, response)

        if response is None or "serviceRoot" not in response:
            self._remove(Settings._service_root)
        else:
            self._set(Settings._service_root, response["serviceRoot"])

        self._save()

    def _get_access_token(self, settings_token_key):
        return [self._get(settings_token_key + Settings._access_token_key),
                self._get(settings_token_key + Settings._access_token_expires_key)]

    def _set_access_token(self, settings_token_key, result):
        if result is None:
            self._remove(settings_token_key + Settings._access_token_key)
            self._remove(settings_token_key + Settings._access_token_expires_key)
        else:
            self._set(settings_token_key + Settings._access_token_key, result["accessToken"])
            self._set(settings_token_key + Settings._access_token_expires_key,
                      self._ticks_from_javascript_datetime(result["accessTokenExpires"]))

    def _ticks_from_javascript_datetime(self, javascript_datetime):
        return re.compile("\/Date\((\d+)\)\/").findall(javascript_datetime)[0]

    @property
    def user_token(self):
        return AccessToken(self._get_access_token(Settings._user_token))

    @property
    def user_id(self):
        return self._get(Settings._user_id)

    def set_user(self, result):
        self._set_access_token(Settings._user_token, result)

        if result is None:
            self._remove(Settings._user_id)
        else:
            self._set(Settings._user_id, result["id"])

        self._save()

    def _save(self):
        with open(Settings._buddy_cfg, "w") as configfile:
            self._settings.write(configfile)

    def _get(self, option):
        if self._settings.has_option(self._app_id, option):
            return self._settings.get(self._app_id, option)
        else:
            return None

    def _set(self, option, value):
        return self._settings.set(self._app_id, option, value)

    def _remove(self, option):
        return self._settings.remove_option(self._app_id, option)