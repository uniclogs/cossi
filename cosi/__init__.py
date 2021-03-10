import os
from datetime import timedelta

# Version Details
MAJOR = 1
MINOR = 0
PATCH = 1

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
DB_HOST = os.getenv('DART_HOST')
DB_PORT = int(os.getenv('DART_PORT', '5432'))
DB_NAME = os.getenv('DART_DB')
DB_USERNAME = os.getenv('DART_USERNAME')
DB_PASSWORD = os.getenv('DART_PASSWORD')

# Satnogs constants
SATNOGS_TOKEN = os.getenv('SATNOGS_DB_TOKEN')
SATNOGS_API = 'https://db.satnogs.org/api'
SATNOGS_SATELITE_ENDPOINT = f'{SATNOGS_API}/satellites/''{}/?format=json'
SATNOGS_TELEMETRY_ENDPOINT = f'{SATNOGS_API}/telemetry/?satellite=' \
                             '{}&format=json'

# Spacetrack (18th-Space) constants
SPACETRACK_USERNAME = os.getenv('SPACETRACK_USERNAME')
SPACETRACK_PASSWORD = os.getenv('SPACETRACK_PASSWORD')
SPACETRACK_API = 'https://www.space-track.org'
SPACETRACK_LOGIN_ENDPOINT = f'{SPACETRACK_API}/ajaxauth/login'
SPACETRACK_TLE_ENDPOINT = f'{SPACETRACK_API}/basicspacedata/query/class/tle/' \
                          'NORAD_CAT_ID/{}/predicates/TLE_LINE0,TLE_LINE1,' \
                          'TLE_LINE2/limit/1/format/json'
STALE_TLE_TIMEOUT = timedelta(days=1)
