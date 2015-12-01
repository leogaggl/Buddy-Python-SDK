from buddy_client import BuddyClient


class BuddyProperties(type):
    @property
    def current_client(cls):
        return Buddy._current_client

    @property
    def current_user_id(cls):
        return Buddy.current_client.current_user_id

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


class Buddy(object, metaclass=BuddyProperties):

    _clients = {}
    _current_client = None

    @staticmethod
    def init(app_id, app_key):

        if Buddy._clients.get(app_id) is None:
            client = BuddyClient(app_id, app_key)
            Buddy._clients[app_id] = client
        else:
            client = Buddy._clients.get(app_id)

        Buddy._current_client = client

        return Buddy.current_client

    @staticmethod
    def delete(path):
        return Buddy.current_client.delete(path)

    @staticmethod
    def get(path):
        return Buddy.current_client.get(path)

    @staticmethod
    def patch(path, dictionary):
        return Buddy.current_client.patch(path, dictionary)

    @staticmethod
    def post(path, dictionary):
        return Buddy.current_client.post(path, dictionary)

    @staticmethod
    def put(path, dictionary):
        return Buddy.current_client.put(path, dictionary)

    @staticmethod
    def create_user(user_name, password, first_name=None, last_name=None, email=None, gender=None, date_of_birth=None, tag=None):
       return Buddy.current_client.create_user(user_name, password, first_name, last_name, email, gender, date_of_birth, tag)

    @staticmethod
    def login_user(user_name, password):
       return Buddy.current_client.login_user(user_name, password)

    @staticmethod
    def logout_user():
        Buddy.current_client.logout_user()