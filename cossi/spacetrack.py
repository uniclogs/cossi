import requests
from . import assert_env, \
              SPACETRACK_USERNAME, \
              SPACETRACK_PASSWORD, \
              SPACETRACK_API, \
              SPACETRACK_LOGIN_ENDPOINT, \
              SPACETRACK_TLE_ENDPOINT, \
              FailedAPIRequest


@assert_env('SPACETRACK_USERNAME')
@assert_env('SPACETRACK_PASSWORD')
def create_spacetrack_session() -> requests.Session:
    """Attempts to open a session with the space-track.org API with given
    credentials

    :raises EnvironmentError: if the environment variable `SPACETRACK_USERNAME`
        is not defined
    :raises EnvironmentError: if the environment variable `SPACETRACK_PASSWORD`
        is not defined
    :raises FailedAPIRequest: if the authentication request to the SpaceTrack
        API failed

    :return: A succesfully authenticated session with API
    :rtype: requests.Session
    """
    endpoint = f'{SPACETRACK_API}{SPACETRACK_LOGIN_ENDPOINT}'
    credentials = {
        'identity': SPACETRACK_USERNAME,
        'password': SPACETRACK_PASSWORD
    }

    session = requests.Session()
    res = session.post(endpoint, credentials)
    if(not res.ok):
        raise FailedAPIRequest(res)
    return session


def request_tle(norad_id: int) -> tuple:
    """Makes a request to space-track.org for the latest TLE of a satellite
    specified by Norad ID.

    :param norad_id: The satellite's unique identifier
    :type norad_id: int

    :raises FailedAPIRequest: if the HTTP request to space-track.org failed

    :return: A tuple of the ordered two-line element
    :rtype: tuple
    """
    with create_spacetrack_session() as session:
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        endpoint = f'{SPACETRACK_API}' \
                   f'{SPACETRACK_TLE_ENDPOINT.format(norad_id)}'
        res = session.get(endpoint, headers=headers)
        if(not res.ok):
            raise FailedAPIRequest(res)

        data = res.json()
        if(len(data) == 0):
            raise FailedAPIRequest(res,
                                   message='No TLE\'s found for NORAD ID'
                                           f' #{norad_id}')
        return tuple(list(data[0].values())[1:])
