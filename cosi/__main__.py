import json
import argparse
from . import APP_NAME, APP_DESCRIPTION
from .satnogs import request_satellite, \
                     request_telemetry, \
                     decode_telemetry_frame
from .spacetrack import request_tle


def main():
    parser = argparse.ArgumentParser(prog=APP_NAME,
                                     description=APP_DESCRIPTION,
                                     allow_abbrev=False)
    parser.add_argument('norad_id',
                        type=int,
                        help='The satellite NORAD ID to search by when'
                             ' fetching TLE\'s or telemetry.')
    parser.add_argument('--get-satellite',
                        dest='get_satellite',
                        action='store_true',
                        default=False,
                        help='Fetch the latest satellite metadata from SatNOGS'
                             ' DB and save it as a JSON file.')
    parser.add_argument('--get-telemetry',
                        dest='get_telemetry',
                        action='store_true',
                        default=False,
                        help='Fetch the latest telemetry from SatNOGS DB and'
                             ' save it as a binary file.')
    parser.add_argument('--get-tle',
                        dest='get_tle',
                        action='store_true',
                        default=False,
                        help='Fetch the latest TLE from Space-Track and save it to file.')
    parser.add_argument('--no-decode',
                        dest='decode',
                        action='store_false',
                        default=True,
                        help='Disable decoding the raw frames if fetching'
                             ' satellite telemetry.')
    parser.add_argument('--satellite-path',
                        dest='satellite_path',
                        type=str,
                        default='./satellite.json',
                        help='Specify the location to write the satellite'
                             ' metadata to. Used in conjunction with'
                             ' `--get-satellite`.')
    parser.add_argument('--telemetry-path',
                        dest='telemetry_path',
                        type=str,
                        default='./telemetry.raw',
                        help='Specify the location to write the raw telemetry'
                             ' to. Used in conjunction with `--get-telemetry`.')
    parser.add_argument('--tle-path',
                        dest='tle_path',
                        type=str,
                        default='./latest.tle',
                        help='Specify the location to write the latest TLE to.'
                             ' Used in conjunction with `--get-tle`.')
    args = parser.parse_args()

    if(args.get_satellite):
        satellite = request_satellite(args.norad_id)
        with open(args.satellite_path, 'w+') as file:
            json.dump(satellite, file, indent=4, sort_keys=True)

    if(args.get_telemetry):
        telemetry = request_telemetry(args.norad_id)
        frame = telemetry.get('frame', None)
        if(frame is None):
            raise ValueError(f'Did not find a raw Frame for Satellite #{args.norad_id}: {telemetry}')
        with open(args.telemetry_path, 'wb+') as file:
            file.write(bytearray.fromhex(frame))

        if(args.decode):
            decoded_frame = decode_telemetry_frame(frame)
            print(f'Decoded frame: {decoded_frame}')
            # TODO: Write to DART database

    if(args.get_tle):
        tle_data = request_tle(args.norad_id)
        tle = '\n'.join(tle_data.values())
        with open(args.tle_path, 'w+') as file:
            file.write(tle)


if __name__ == '__main__':
    main()
