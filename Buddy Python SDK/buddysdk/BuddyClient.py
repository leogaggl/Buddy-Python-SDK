#import python-hwinfo
import requests
import events
import threading
import Connection


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
        self._connectivity_changed = events.Events()
        self._connectivity_retry = threading.Thread(target = self.__connectivity_retry)
        self._connectivity_level = Connection.Connection.Connection

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
    def connectivity_changed(self):
        return self._connectivity_changed

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
        if response is not None:
            return response.json()['result']
        else:
            return None

    def __handle_http_exception(self, exception):
        pass

    def __handle_connection_exception(self, exception):
        self.__set_connectivity_level(Connection.Connection.NoConnection)

        if not self._connectivity_retry.isAlive():
            self._connectivity_retry.start()

    def __connectivity_retry(self):
        success = False

        while not success:
            try:
                response = requests.post(self._settings.service_root + "/service/ping")
                success = True
            except requests.exceptions.RequestException:
                success = False
            except requests.exceptions.ConnectionError:
                success = False
            except requests.exceptions.HTTPError:
                success = False
            except requests.exceptions.URLRequired:
                success = False
            except requests.exceptions.Timeout:
                success = False

        self.__set_connectivity_level(Connection.Connection.Connection)

    def __set_connectivity_level(self, connectivity_level):
        if self._connectivity_level != connectivity_level:
            self._connectivity_level = connectivity_level
            self._connectivity_changed.on_change(self._connectivity_level)


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
