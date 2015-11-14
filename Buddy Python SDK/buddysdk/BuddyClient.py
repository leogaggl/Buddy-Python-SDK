#import python-hwinfo
import requests
import events
import threading
from Connection import Connection


class BuddyClient(object):
    def __init__(self, app_id, app_key, settings):
        self._app_id = app_id
        self._app_key = app_key

        self._settings = settings
        self._session = requests.Session()
        self._session.auth = Auth(self, self._settings)
        self._last_location = None

        self._service_exception = events.Events()
        self._authentication_changed = events.Events()
        self._connection_changed = events.Events()
        self._connection_retry = threading.Thread(target = self.__connection_retry)
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

    def register_device(self):
        response = self.__handle_request(requests.post, "/devices", {
            "platform" : "Raspberry Pi",
            "model" : self.__get_model(),
            "osVersion" : self.__get_os_version(),
            "uniqueId" : self.__get_serial(),
            "appid" : self.app_id,
            "appkey" : self.app_key
        })

        self._settings.process_device_registration(response)

    def __get_serial(self):
        cpuserial = "0000000000000000"
        try:
            f = open('/proc/cpuinfo', 'r')
            for line in f:
                if line[0:6] == 'Serial':
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

    def __handle_request(self, method, path, dictionary):
        response = None

        try:
            response = method(self._settings.service_root + path, json = dictionary)
        except requests.exceptions.RequestException as ex:
            self.__handle_connection_exception(ex)
        except requests.exceptions.ConnectionError as ex:
            self.__handle_connection_exception(ex)
        except requests.exceptions.HTTPError as ex:
            self.__handle_http_exception(ex)
        except requests.exceptions.URLRequired as ex:
            self.__handle_http_exception(ex)
        except requests.exceptions.Timeout as ex:
            self.__handle_connection_exception(ex)

        return self.__handle_response(response)

    def __handle_response(self, response):
        if response is None:
            return None
        else:
            return response.json()['result']

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
                response = requests.post(self._settings.service_root + "/service/ping")
                successful = True
            except requests.exceptions.RequestException:
                successful = False
            except requests.exceptions.ConnectionError:
                successful = False
            except requests.exceptions.HTTPError:
                successful = False
            except requests.exceptions.URLRequired:
                successful = False
            except requests.exceptions.Timeout:
                successful = False

        self.__set_connection_level(Connection.On)

    def __set_connection_level(self, connection_level):
        if self._connection_level != connection_level:
            self._connection_level = connection_level
            self._connection_changed.on_change(self._connection_level)


class Auth(requests.auth.AuthBase):

    def __init__(self, client, settings):
        self._client = client
        self._settings = settings

    def __call__(self, request):
        if self._settings.access_token == "":
            self._client.register_device()
            #pass

        #request.headers["Authorization"] = "Buddy eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOiIyMDE1LTExLTExVDAzOjM0OjU4LjE2Mjg2NzlaIiwibCI6ImJiYmJ2LnJwZGJ2eGJnR3JNZyIsImEiOiJiYmJiYmMueGdqYnZQZHdrbGx3IiwidSI6bnVsbCwiZCI6ImJsai5sRHBGd0tNc2dGRk0ifQ.l4ob5liSYfgI25mnysjRHpgCYr1yCzayC4XjHJOv4v0"
        request.headers["Authorization"] = "Buddy " + self._settings.access_token

        return request
