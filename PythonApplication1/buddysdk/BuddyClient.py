import datetime
import requests
#import python-hwinfo
from . import Settings


class BuddyClient(object):
    def __init__(self, app_id, app_key, settings):
        self._app_id = app_id
        self._app_key = app_key
        self._settings = settings
        self._session = requests.Session()
        self._session.auth = Auth(self, self._settings)

    @property
    def app_id(self):
        return self._app_id

    @property
    def app_key(self):
        return self._app_key

    def get_serial(self):
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

    def register_device(self):
    
        response = requests.post(self._settings.service_root + "/devices", json = {
            "platform" : "Raspberry Pi",
            "model" : "model",
            "osVersion" : "",
            "uniqueId" : self.get_serial(),
            "appid" : self.app_id,
            "appkey" : self.app_key
        })

        self._settings.process_device_registration(self.handle_response(response.json()))

    def post(self, path, dictionary):
        return self.handle_request(self._session.post, path, dictionary)

    def put(self, path, dictionary):
        return self.handle_request(self._session.put, path, dictionary)

    def handle_request(self, method, path, dictionary):
        try:
            response = method(self._settings.service_root + path, json = dictionary)
        except requests.exceptions.RequestException:
            pass
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.HTTPError:
            pass
        except requests.exceptions.URLRequired:
            pass
        except requests.exceptions.Timeout:
            pass

        return self.handle_response(response.json())

    def handle_response(self, json):
        result = json['result']
        return result


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
