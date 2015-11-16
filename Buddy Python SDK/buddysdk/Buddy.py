from buddy_client import BuddyClient
from settings import Settings


class BuddyProperties(type):
    @property
    def current_client(cls):
        return Buddy._current_client

    @property
    def last_location(cls):
        return Buddy.current_client.last_location

    @last_location.setter
    def last_location(cls, value):
    		Buddy.current_client.last_location = value

    @property
    def service_exception(cls):
        return Buddy.current_client.service_exception

    @property
    def authentication_changed(cls):
        return Buddy.current_client.authentication_changed

    @property
    def connection_changed(cls):
        return Buddy.current_client.connection_changed


class Buddy(object, metaclass = BuddyProperties):

    _clients = {}
    _current_client = None

    @staticmethod
    def init(app_id, app_key, settings = None):

        settings = settings if settings is not None else Settings(app_id)

        if Buddy._clients.get(app_id) is None:
            client = BuddyClient(app_id, app_key, settings)
            Buddy._clients[app_id] = client
        else:
            client = Buddy._clients.get(app_id)

        Buddy._current_client = client

        return Buddy.current_client

    @staticmethod
    def post(path, dictionary):
        return Buddy.current_client.post(path, dictionary)

    @staticmethod
    def put(path, dictionary):
        return Buddy.current_client.put(path, dictionary)

    @staticmethod
    def create_user(dictionary):
       return Buddy.current_client.create_user(dictionary)

    @staticmethod
    def login_user(dictionary):
       return Buddy.current_client.login_user(dictionary)

    @staticmethod
    def logout_user(dictionary):
       return Buddy.current_client.logout_user(dictionary)

    @staticmethod
    def get_current_user(self):
        return Buddy.current_client.get_current_user()