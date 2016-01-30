from events import Events
import platform
import requests
import sys
from threading import Thread
import uuid

from connection import Connection
from settings import Settings


class BuddyClient(object):
    result_name = "result"
    _hardware_info_file_name = "/proc/cpuinfo"

    def __init__(self, app_id, app_key):
        self._app_id = app_id
        self._app_key = app_key

        self._settings = Settings(self._app_id)
        self._session = requests.Session()
        self._session.auth = Auth(self, self._settings)
        self._last_location = None

        self._service_exception = Events()
        self._authentication_needed = Events()
        self._connection_changed = Events()
        self._connection_retry = Thread(target=self.__connection_retry_method)
        self._connection_level = Connection.on

    @property
    def app_id(self):
        return self._app_id

    @property
    def app_key(self):
        return self._app_key

    @property
    def last_location(self):
        return self._last_location

    @last_location.setter
    def last_location(self, value):
        self._last_location = value

    @property
    def current_user_id(self):
        return self._settings.user_id

    @property
    def service_exception(self):
        return self._service_exception

    @property
    def authentication_needed(self):
        return self._authentication_needed

    @property
    def connection_changed(self):
        return self._connection_changed

    def get_access_token_string(self):
        if self._settings.access_token_string is None:
            self.__register_device()

        return self._settings.access_token_string

    def __register_device(self):
        response = self.__handle_dictionary_request(requests.post, "/devices", {
            "appId": self.app_id,
            "appKey": self.app_key,
            "platform": BuddyClient.__get_platform(),
            "model": BuddyClient.__get_model(),
            "osVersion": BuddyClient.__get_os_version(),
            "uniqueId": self.__get_unique_id(),
        })

        if response is not None:
            self._settings.set_device_token(response[BuddyClient.result_name])

    @staticmethod
    def __get_platform():
        return sys.platform

    @staticmethod
    def __get_model():
        hardware = BuddyClient.__get_cpuinfo("Hardware")
        revision = BuddyClient.__get_cpuinfo("Revision")
        if hardware is None:
            return "Hardware info not available"
        else:
            return hardware + "-" + revision

    @staticmethod
    def __get_os_version():
        return platform.release()

    def __get_unique_id(self):
        unique_id = BuddyClient.__get_cpuinfo("Serial")
        if unique_id is None:
            unique_id = uuid.getnode()
        return unique_id

    @staticmethod
    def __get_cpuinfo(key):
        try:
            with open(BuddyClient._hardware_info_file_name, "r") as hardware_file:
                for line in hardware_file:
                    if line.startswith(key):
                        return line.splitlines()[0].split(": ")[1]
        except:
            return None

    def get(self, path, parameters):
        return self.__handle_parameters_request(self._session.get, path, parameters)

    def delete(self, path, parameters):
        return self.__handle_parameters_request(self._session.delete, path, parameters)

    def patch(self, path, dictionary):
        return self.__handle_dictionary_request(self._session.patch, path, dictionary)

    def post(self, path, dictionary, file=None):
        return self.__handle_dictionary_request(self._session.post, path, dictionary, file)

    def put(self, path, dictionary):
        return self.__handle_dictionary_request(self._session.put, path, dictionary)

    def create_user(self, user_name, password, first_name=None, last_name=None, email=None, gender=None, date_of_birth=None, tag=None):
        response = self.__handle_dictionary_request(self._session.post, "/users", {
            "username": user_name,
            "password": password,
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "gender": gender,
            "dateOfBirth": date_of_birth,
            "tag": tag
        })

        if response is not None:
            self._settings.set_user(response[BuddyClient.result_name])

        return response

    def login_user(self, user_name, password):
        response = self.__handle_dictionary_request(self._session.post, "/users/login", {
            "username": user_name,
            "password": password,
        })

        if response is not None:
            self._settings.set_user(response[BuddyClient.result_name])

        return response

    def logout_user(self):
        self._settings.set_user(None)

    def __handle_parameters_request(self, verb, path, parameters=None):
        self.__handle_last_location(parameters)

        def closure():
            return verb(self._settings.service_root + path, params=parameters)

        return self.__handle_request(closure)

    def __handle_dictionary_request(self, verb, path, dictionary, file=None):
        self.__handle_last_location(dictionary)

        def closure():
            if file is None:
                return verb(self._settings.service_root + path, json=dictionary)
            else:
                return verb(self._settings.service_root + path, json=dictionary, files={"data": ("data",) + file})

        return self.__handle_request(closure)

    def __handle_last_location(self, dictionary):
        if self.last_location is not None and dictionary is not None:
            dictionary["location"] = "%s, %s" % self.last_location

    def __handle_request(self, closure):
        response = None

        try:
            response = closure()
        except requests.RequestException:
            self.__handle_connection_exception()
        finally:
            return self.__handle_response(response)

    def __handle_response(self, response):
        if response is None:
            return None
        else:
            if response.status_code == 401 or response.status_code == 403:
                self._authentication_needed.on_change()

            return response.json()

    def __handle_connection_exception(self):
        self.__set_connection_level(Connection.off)

        if not self._connection_retry.isAlive():
            self._connection_retry.start()

    def __connection_retry_method(self):
        successful = False

        try:
            while not successful:
                try:
                    requests.get(self._settings.service_root + "/service/ping")
                except requests.RequestException:
                    successful = False
                else:
                    successful = True
        finally:
            self.__set_connection_level(Connection.on)

    def __set_connection_level(self, connection_level):
        if self._connection_level is not connection_level:
            self._connection_level = connection_level
            self._connection_changed.on_change(self._connection_level)


class Auth(requests.auth.AuthBase):

    def __init__(self, client, settings):
        self._client = client
        self._settings = settings

    def __call__(self, request):
        access_token = self._client.get_access_token_string()

        if access_token is not None:
            request.headers["Authorization"] = "Buddy " + access_token

        return request
