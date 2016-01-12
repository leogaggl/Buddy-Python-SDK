from datetime import datetime


class AccessToken(object):
    def __init__(self, values):
        if values is None or values is "":
            self._token = ""
            self._set_expires(None)
        else:
            self._token = values[0]
            self._set_expires(values[1])

    @property
    def token(self):
        if self._token is None or self._token is "" or self._expires <= datetime.utcnow():
            return None
        else:
            return self._token

    @property
    def expires(self):
        return self._expires

    def _set_expires(self, value):
        if value is None or value is "":
            self._expires = datetime.utcfromtimestamp(0)
        else:
            ticks = int(float(value))
            timestamp = self._timestamp_from_ticks(ticks)
            self._expires = datetime.utcfromtimestamp(timestamp)

    def _timestamp_from_ticks(self, ticks):
        return ticks / 1000