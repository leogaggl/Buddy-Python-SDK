from . import BuddyClient
from . import Settings


class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


class Buddy(object):

    _clients = {}
    _current_client = None

    def __init__(self):
        pass

    @staticmethod
    def init(app_id, app_key):

        if Buddy._clients.get(app_id) != None:
            client = Buddy._clients.get(app_id)
        else:
            client = BuddyClient.BuddyClient(app_id, app_key, Settings.Settings(app_id))
            Buddy._clients[app_id] = client

        Buddy.current_client = client

        return Buddy.current_client

    @classproperty
    def current_client(cls):
        return cls._current_client

