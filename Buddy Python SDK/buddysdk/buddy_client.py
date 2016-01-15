from events import Events
import platform
import requests
from threading import Thread

from connection import Connection
from settings import Settings


class BuddyClient(object):
    result = "result"
    _hardware_info_file = "/proc/cpuinfo"

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
        self._connection_retry = Thread(target=self._connection_retry_method)
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
            self._register_device()

        return self._settings.access_token_string

    def _register_device(self):
        response = self._handle_dictionary_request(requests.post, "/devices", {
            "appId": self.app_id,
            "appKey": self.app_key,
            "platform": self._get_platform(),
            "model": self._get_model(),
            "osVersion": self._get_os_version(),
            "uniqueId": self._get_unique_id(),
        })

        self._settings.set_device_token(response[BuddyClient.result])

    def _get_platform(self):
        return "Raspberry Pi"

    def _get_model(self):
        hardware = self._get_cpuinfo("Hardware")
        revision = self._get_cpuinfo("Revision")
        if hardware is None:
            return "Raspberry Pi"
        else:
            return hardware + "-" + revision

    def _get_os_version(self):
        return platform.release()

    def _get_unique_id(self):
        unique_id = self._get_cpuinfo("Serial")
        if unique_id is None:
            unique_id = "ERROR000000000"
        return unique_id

    def _get_cpuinfo(self, key):
        try:
            with open(BuddyClient._hardware_info_file, "r") as file:
                for line in file:
                    if line.startswith(key):
                        return line.splitlines()[0].split(": ")[1]
        except:
            return None

    def get(self, path, parameters):
        return self._handle_parameters_request(self._session.get, path, parameters)

    def delete(self, path, parameters):
        return self._handle_parameters_request(self._session.delete, path, parameters)

    def patch(self, path, dictionary):
        return self._handle_dictionary_request(self._session.patch, path, dictionary)

    def post(self, path, dictionary, file=None):
        return self._handle_dictionary_request(self._session.post, path, dictionary, file)

    def put(self, path, dictionary):
        return self._handle_dictionary_request(self._session.put, path, dictionary)

    def create_user(self, user_name, password, first_name=None, last_name=None, email=None, gender=None, date_of_birth=None, tag=None):
        response = self._handle_dictionary_request(self._session.post, "/users", {
            "username": user_name,
            "password": password,
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "gender": gender,
            "dateOfBirth": date_of_birth,
            "tag": tag
        })

        self._settings.set_user(response[BuddyClient.result])

        return response

    def login_user(self, user_name, password):
        response = self._handle_dictionary_request(self._session.post, "/users/login", {
            "username": user_name,
            "password": password,
        })

        self._settings.set_user(response[BuddyClient.result])

        return response

    def logout_user(self):
        self._settings.set_user(None)

    def _handle_parameters_request(self, verb, path, parameters=None):
        self._handle_last_location(parameters)

        def closure():
            return verb(self._settings.service_root + path, params=parameters)

        return self._handle_request(closure)

    def _handle_dictionary_request(self, verb, path, dictionary, file=None):
        self._handle_last_location(dictionary)

        def closure():
            if file is None:
                return verb(self._settings.service_root + path, json=dictionary)
            else:
                return verb(self._settings.service_root + path, json=dictionary, files={"data": ("data",) + file})

        return self._handle_request(closure)

    def _handle_last_location(self, dict):
        if self.last_location is not None and dict is not None:
            dict["location"] = self.last_location

    def _handle_request(self, closure):
        response = None

        try:
            response = closure()
        except requests.RequestException:
            self._handle_connection_exception()
        finally:
            return self._handle_response(response)

    def _handle_response(self, response):
        if response is None:
            return None
        else:
            if response.status_code == 401 or response.status_code == 403:
                self._authentication_needed.on_change()

            return response.json()

    def _handle_connection_exception(self):
        self._set_connection_level(Connection.off)

        if not self._connection_retry.isAlive():
            self._connection_retry.start()

    def _connection_retry_method(self):
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
            self._set_connection_level(Connection.on)

    def _set_connection_level(self, connection_level):
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
