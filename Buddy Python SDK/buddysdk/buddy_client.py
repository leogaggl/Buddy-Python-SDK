from events import Events
import requests
from threading import Thread
from connection import Connection
from settings import Settings


class BuddyClient(object):
    def __init__(self, app_id, app_key):

        self._app_id = app_id
        self._app_key = app_key

        self._settings = Settings(self._app_id)
        self._session = requests.Session()
        self._session.auth = Auth(self, self._settings)
        self._last_location = None

        self._service_exception = Events()
        self._authentication_changed = Events()
        self._connection_changed = Events()
        self._connection_retry = Thread(target=self.__connection_retry)
        self._connection_level = Connection.On

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
    def service_exception(self):
        return self._service_exception

    @property
    def authentication_changed(self):
        return self._authentication_changed

    @property
    def connection_changed(self):
        return self._connection_changed

    def get_access_token_string(self):
        if self._settings.access_token_string is None:
            self.__register_device()

        return self._settings.access_token_string

    def __register_device(self):
        response = self.__handle_request(requests.post, "/devices", {
            "appID": self.app_id,
            "appKey": self.app_key,
            "platform": "Raspberry Pi",
            "model": self.__get_model(),
            "osVersion": self.__get_os_version(),
            "uniqueId": self.__get_serial(),
        })

        self._settings.set_device_token(response)

    def __get_serial(self):
        cpuserial = "0000000000000000"
        try:
            f = open("/proc/cpuinfo", 'r')
            for line in f:
                if line[0:6] == "Serial":
                    cpuserial = line[10:26]
            f.close()
        except:
            cpuserial = "ERROR000000000"
        return cpuserial

    def __get_model(self):
        return "model"

    def __get_os_version(self):
        return "os_version"

    def post(self, path, dictionary):
        return self.__handle_request(self._session.post, path, dictionary)

    def put(self, path, dictionary):
        return self.__handle_request(self._session.put, path, dictionary)

    def create_user(self, user_name, password, first_name, last_name, email, gender, date_of_birth, tag):
        response = self.__handle_request(self._session.post, "/users",
            {
                "username": user_name,
                "password": password,
                "firstName": first_name,
                "lastName": last_name,
                "email": email,
                "gender": gender,
                "dateOfBirth": date_of_birth,
                "tag": tag
            })

        self._settings.set_user_token(response)

    def login_user(self, user_name, password):
        response = self.__handle_request(self._session.post, "/users",
            {
                "username": user_name,
                "password": password,
            })

        self._settings.set_user_token(response)

    def logout_user(self):
        self._settings.set_user_token(None)

    def __handle_request(self, method, path, dictionary):
        response = None

        try:
            response = method(self._settings.service_root + path, json=dictionary)
        except requests.ConnectionError as ex:
            self.__handle_connection_exception(ex)
        except requests.HTTPError as ex:
            self.__handle_http_exception(ex)
        except requests.URLRequired as ex:
            self.__handle_http_exception(ex)
        except requests.Timeout as ex:
            self.__handle_connection_exception(ex)

        return self.__handle_response(response)

    def __handle_response(self, response):
        if response is None:
            return None
        else:
            #if response.status_code is 401 or response.status_code is 403
            json = response.json()
            if "result" in json:
                return json["result"]
            else:
                return None

    def __handle_http_exception(self, exception):
        pass

    def __handle_connection_exception(self, exception):
        self.__set_connection_level(Connection.Off)

        if not self._connection_retry.isAlive():
            self._connection_retry.start()

    def __connection_retry(self):
        successful = False

        while not successful:
            try:
                requests.get(self._settings.service_root + "/service/ping")
                successful = True
            except requests.ConnectionError:
                successful = False
            except requests.HTTPError:
                successful = False
            except requests.URLRequired:
                successful = False
            except requests.Timeout:
                successful = False

        self.__set_connection_level(Connection.On)

    def __set_connection_level(self, connection_level):
        if self._connection_level is not connection_level:
            self._connection_level = connection_level
            self._connection_changed.on_change(self._connection_level)


class Auth(requests.auth.AuthBase):

    def __init__(self, client, settings):
        self._client = client
        self._settings = settings

    def __call__(self, request):
        #request.headers["Authorization"] = "Buddy eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOiIyMDE1LTExLTExVDAzOjM0OjU4LjE2Mjg2NzlaIiwibCI6ImJiYmJ2LnJwZGJ2eGJnR3JNZyIsImEiOiJiYmJiYmMueGdqYnZQZHdrbGx3IiwidSI6bnVsbCwiZCI6ImJsai5sRHBGd0tNc2dGRk0ifQ.l4ob5liSYfgI25mnysjRHpgCYr1yCzayC4XjHJOv4v0"
        access_token = self._client.get_access_token_string()

        if access_token is not None:
            request.headers["Authorization"] = "Buddy " + access_token

        return request
