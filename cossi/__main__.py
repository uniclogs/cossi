import json
import argparse
from . import APP_NAME, APP_DESCRIPTION
from .decoders import Decoder
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
    parser.add_argument('--decode', '-d',
                        dest='decoder',
                        type=str.upper,
                        choices={'CSIM', 'OREFLAT0', 'ORESAT0'},
                        help='Attempt to decode telemetry fetched from SatNOGS'
                             ' DB.')
    parser.add_argument('--decode-output', '--do',
                        dest='decoded_data_output',
                        type=str,
                        default='./decoded.json',
                        help='Specify decoded data output path. [Default:'
                             ' ./decoded.json]')
    parser.add_argument('--satellite-metadata', '-s',
                        dest='get_satellite',
                        action='store_true',
                        default=False,
                        help='Fetch the latest satellite metadata from SatNOGS'
                             ' DB.')
    parser.add_argument('--satellite-metadata-output', '--so',
                        dest='satellite_meta_output',
                        type=str,
                        default='./satellite.json',
                        help='Specify satellite metadata output path.'
                             ' [Default: ./satellite.json]')
    parser.add_argument('--satnogs-dev', '--sd',
                        dest='satnogs_dev',
                        action='store_true',
                        default=False,
                        help='Toggle the API endpoint for SatNOGS to [db-dev]'
                             ' and [network-dev] instead of [db] and'
                             ' [network].')
    parser.add_argument('--telemetry', '-t',
                        dest='get_telemetry',
                        action='store_true',
                        default=False,
                        help='Fetch the latest telemetry from SatNOGS DB.')
    parser.add_argument('--telemetry-output', '--to',
                        dest='telemetry_output',
                        type=str,
                        default='./telemetry.json',
                        help='Specify telemetry output path. [Default:'
                             ' ./telemetry.json]')
    parser.add_argument('--tle', '-o',
                        dest='get_tle',
                        action='store_true',
                        default=False,
                        help='Fetch the latest TLE from SpaceTrack.')
    parser.add_argument('--tle-output', '--oo',
                        dest='tle_output',
                        type=str,
                        default='./latest.tle',
                        help='Specify TLE output path. [Default:'
                             ' ./latest.tle]')
    args = parser.parse_args()

    if(args.get_satellite):
        satellite = request_satellite(args.norad_id,
                                      satnogs_dev=args.satnogs_dev)
        with open(args.satellite_meta_output, 'w+') as file:
            json.dump(satellite, file, indent=4, sort_keys=True)

    if(args.get_telemetry):
        telemetry = request_telemetry(args.norad_id,
                                      satnogs_dev=args.satnogs_dev)
        frame = telemetry.get('frame', None)

        if(frame is None):
            raise ValueError('Did not find a raw Frame for Satellite'
                             f' #{args.norad_id}: {telemetry}')
        with open(args.telemetry_output, 'w+') as file:
            json.dump(telemetry, file, indent=4, sort_keys=True)

        if(args.decoder):
            decoded_data = decode_telemetry_frame(frame, Decoder[args.decoder])
            with open(args.decoded_data_output, 'w+') as file:
                json.dump(decoded_data, file, indent=4, sort_keys=True)

    if(args.get_tle):
        tle = request_tle(args.norad_id)
        with open(args.tle_output, 'w+') as file:
            for t in tle:
                file.write(t + '\n')


if __name__ == '__main__':
    main()
