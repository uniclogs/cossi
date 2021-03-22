from functools import wraps
from os import environ, getenv

# Version Details
MAJOR = 2
MINOR = 0
PATCH = 0

# Application information
APP_NAME = 'uniclogs-cosi'
APP_VERSION = f'{MAJOR}.{MINOR}.{PATCH}'
APP_AUTHOR = 'Dmitri McGuckin'
APP_LICENSE = 'GPLv3'
APP_DESCRIPTION = 'Cosmos Satnogs/SpaceTrack Interface. An application for' \
                  ' fetching the latest relevant satellite metadata and' \
                  ' telemetry from SatNOGSs\' and Space-Tracks\' API\'s'
APP_URL = 'https://github.com/oresat/uniclogs-cosi'

# Dart DB constants
DB_HOST = getenv('DART_HOST')
DB_PORT = int(getenv('DART_PORT', '5432'))
DB_NAME = getenv('DART_DB')
DB_USERNAME = getenv('DART_USERNAME')
DB_PASSWORD = getenv('DART_PASSWORD')

# Satnogs constants
SATNOGS_TOKEN = getenv('SATNOGS_DB_TOKEN')
SATNOGS_API = 'https://db.satnogs.org/api'
SATNOGS_DEV_API = 'https://db-dev.satnogs.org/api'
SATNOGS_SATELITE_ENDPOINT = '/satellites'
SATNOGS_TELEMETRY_ENDPOINT = '/telemetry'

# Spacetrack (18th-Space) constants
SPACETRACK_USERNAME = getenv('SPACETRACK_USERNAME')
SPACETRACK_PASSWORD = getenv('SPACETRACK_PASSWORD')
SPACETRACK_API = 'https://www.space-track.org'
SPACETRACK_LOGIN_ENDPOINT = '/ajaxauth/login'
SPACETRACK_TLE_ENDPOINT = '/basicspacedata/query/class/tle/NORAD_CAT_ID/{}/' \
                          'predicates/TLE_LINE0,TLE_LINE1,TLE_LINE2/limit/1/' \
                          'format/json'

# Miscellaneous
_PRIMITIVES = (bool, int, str, bytes, dict, list, None)


class FailedAPIRequest(Exception):
    """An error specification for API requests that failed

    :param response: The HTTP response from the API
    :type response: requests.Response

    :param message: Error message
    :type message: str
    """
    def __init__(self, response, message: str = None):
        self.response = response
        self.message = message or self.response.reason

    def __str__(self) -> str:
        return f'[{self.response.request.method}' \
               f' {self.response.status_code}]:' \
               f' {self.message}\n\t{self.response.url}'


def assert_env(env_name: str) -> callable:
    """A decorator for asserting an environment variable's existance.

    :param env_name: The environment varialbe to assert on
    :type env_name: str

    :raises EnvironmentError: if the specified environment variable is not
        defined

    :returns: the decorated function
    :rtype: callable
    """
    def decorate(callback: callable):
        @wraps(callback)
        def wrapper(*args, **kwargs):
            if(env_name not in environ):
                raise EnvironmentError(f'Environment Variable {env_name}'
                                       ' expected but not defined!')
            return callback(*args, **kwargs)
        return wrapper
    return decorate


def dictify(obj: object,
            depth: int = 10,
            ignore_private: bool = False) -> dict:
    """Converts any serialized python object into a dict.

    :param obj: The serialized object to convert
    :type obj: object

    :param depth: The maximum depth of recursion allowed in "dict-ifying" the
        object.
    :type depth: int

    :param ignore_private: Toggle ignoring private fields on the serialized
        object. (Fields that start with `_` are considered private).
    :type ignore_private: bool

    :return: A dictionary representation of the serialized object.
    :rtype: dict
    """
    if(not obj):
        return {}

    res = {}
    for name, value in obj.__dict__.items():
        if(name.startswith('_') and ignore_private):
            continue
        value = dictify(value, depth - 1) \
            if (type(value) not in _PRIMITIVES and depth > 0) \
            else str(value)
        res[name] = value
    return res
