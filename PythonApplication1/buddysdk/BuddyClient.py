import datetime
import requests
#import python-hwinfo
from . import Settings


class BuddyClient(object):
    def __init__(self, app_id, app_key, settings):
        self._app_id = app_id
        self._app_key = app_key
        self._settings = settings

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

        self._settings.process_device_registration(response.json()['result'])

