import requests
from .decoders import Oreflat0
from . import assert_env, \
              dictify, \
              SATNOGS_DB_TOKEN, \
              SATNOGS_API, \
              SATNOGS_DEV_API, \
              SATNOGS_SATELITE_ENDPOINT, \
              SATNOGS_TELEMETRY_ENDPOINT, \
              FailedAPIRequest


@assert_env('SATNOGS_DB_TOKEN')
def request_satellite(norad_id: int = None, satnogs_dev: bool = False) -> dict:
    """Makes a request to db[-dev].satnogs.org for metadata on the satellite
    specified by Norad ID.

    :param norad_id: The satellite's unique identifier
    :type norad_id: int

    :param satnogs_dev: Enables the use of db-dev.satnogs.org instead of
        db.satnogs.org
    :type satnogs_dev: bool

    :raises EnvironmentError: if the environment variable `SATNOGS_DB_TOKEN` is
        not defined
    :raises EnvironmentError: if the HTTP requst to SatNOGS failed

    :return: A python dictionary containing useful metadata about the satellite
    :rtype: dict
    """
    headers = {
        'Authorization': "Token " + SATNOGS_DB_TOKEN,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    parameters = {
        'format': 'json',
        'satellite': str(norad_id)
    }
    api = SATNOGS_DEV_API if satnogs_dev else SATNOGS_API
    endpoint = f'{api}{SATNOGS_SATELITE_ENDPOINT}/{norad_id}'
    response = requests.get(endpoint,
                            headers=headers,
                            params=parameters,
                            allow_redirects=True)
    if(not response.ok):
        raise FailedAPIRequest(response)
    return response.json()


@assert_env('SATNOGS_DB_TOKEN')
def request_telemetry(norad_id: int, satnogs_dev: bool = False) -> dict:
    """Makes a request to db[-dev].satnogs.org for telemetry from the latest
    observation of a satellite specified by Norad ID.

    :param norad_id: The satellite's unique identifier
    :type norad_id: int

    :param satnogs_dev: Enables the use of db-dev.satnogs.org instead of
        db.satnogs.org
    :type satnogs_dev: bool

    :raises EnvironmentError: if the environment variable `SATNOGS_DB_TOKEN` is
        not defined
    :raises FailedAPIRequest: if no telemetry exists for the given satellite
    :raises FailedAPIRequest: if the HTTP request to SatNOGS failed

    :return: A dictionay containing the latest observation of the given
        satellite
    :rtype: dict
    """
    headers = {
        'Authorization': "Token " + SATNOGS_DB_TOKEN,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    parameters = {
        'format': 'json',
        'satellite': str(norad_id)
    }
    api = SATNOGS_DEV_API if satnogs_dev else SATNOGS_API
    endpoint = f'{api}{SATNOGS_TELEMETRY_ENDPOINT}'
    response = requests.get(endpoint,
                            headers=headers,
                            params=parameters,
                            allow_redirects=True)
    if(not response.ok):
        raise FailedAPIRequest(response)
    elif(len(response.json()) == 0):
        raise FailedAPIRequest(response,
                               f'No telemetry for NORAD ID #{norad_id}')
    observations = sorted(response.json(),
                          key=lambda x: x['timestamp'],
                          reverse=True)
    return observations[0]


def decode_telemetry_frame(hex_frame: str) -> dict:
    """Takes a hex-string of telemetry and decodes it using the default
    Oreflat0 Decoder.

    :param hex_frame: The telemetry frame as a hex string
    :type hex_frame: str

    :param decoder: The decoder to use
    :type decoder: str

    :raises ValueError: if the decoder did not find the expected payload

    :return: A dctionary of the decoded data
    :rtype: dict
    """
    raw_bytes = bytearray.fromhex(hex_frame)
    payload = Oreflat0.from_bytes(raw_bytes) \
                      .ax25_frame \
                      .payload.ax25_info
    if(not payload):
        raise ValueError('No payload found!')
    return dictify(payload, depth=3, ignore_private=True)
