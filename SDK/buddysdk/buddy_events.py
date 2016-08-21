from events import Events


class BuddyEvents(object):

    def __init__(self):
        self._service_exception = Events()
        self._user_authentication_needed = Events()
        self._connection_changed = Events()

    @property
    def service_exception(self):
        return self._service_exception

    @property
    def user_authentication_needed(self):
        return self._user_authentication_needed

    @property
    def connection_changed(self):
        return self._connection_changed
