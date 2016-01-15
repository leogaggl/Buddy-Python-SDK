from buddy_client import BuddyClient


__clients = {}
__current_client = None


@property
def current_client(module):
    return __current_client


@property
def current_user_id(module):
    return __current_client.current_user_id


@property
def last_location(module):
    return __current_client.last_location


@last_location.setter
def last_location(module, value):
    __current_client.last_location = value


@property
def service_exception(module):
    return __current_client.service_exception


@property
def authentication_needed(module):
    return __current_client.authentication_needed


@property
def connection_changed(module):
    return __current_client.connection_changed


def init(module, app_id, app_key, instance_name=None):
    global __clients, __current_client

    index = app_id if instance_name is None else app_id + instance_name

    if __clients.get(index) is None:
        __current_client = BuddyClient(app_id, app_key)
        __clients[index] = __current_client
    else:
        __current_client = __clients.get(index)

    return __current_client


def delete(module, path, parameters=None):
    return __current_client.delete(path, parameters)


def get(module, path, parameters=None):
    return __current_client.get(path, parameters)


def patch(module, path, dictionary):
    return __current_client.patch(path, dictionary)


def post(module, path, dictionary, file=None):
    return __current_client.post(path, dictionary, file)


def put(module, path, dictionary):
    return __current_client.put(path, dictionary)


def create_user(module, user_name, password, first_name=None, last_name=None, email=None, gender=None, date_of_birth=None, tag=None):
    return __current_client.create_user(user_name, password, first_name, last_name, email, gender, date_of_birth, tag)


def login_user(module, user_name, password):
    return __current_client.login_user(user_name, password)


def logout_user(module):
    __current_client.logout_user()


import mprop; mprop.init()
