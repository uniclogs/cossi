import os
import unittest
import cosi.satnogs as satnogs
from cosi import FailedAPIRequest
from unittest.mock import MagicMock


class Satnogs_Spec(unittest.TestCase):
    """Tests for the CoSSI-SatNOGS interface"""

    def setUp(self):
        self.norad_id = 99910  # OreFLAT NORAD ID

        # Monkeypatch the request library with a mock
        self.mock_requests = MagicMock()
        self.old_requests = satnogs.requests
        satnogs.requests = self.mock_requests

        # Create fake telemetry frame
        self.fake_frame = {
            "app_source": "network",
            "decoded": "",
            "frame": "A6A082868A406096946EA682A86103F03A4B4A37534154202D205465737420626561636F6E2066726F6D20415835303433206472697665722E2053756E204A616E2031332032313A33383A353220313938300A",
            "norad_cat_id": 99910,
            "observation_id": 31534,
            "observer": "FLATNOGS-CN85pm",
            "schema": "",
            "station_id": 326,
            "timestamp": "2021-03-21T19:24:31Z",
            "transmitter": "",
            "version": ""
        }

        # Create fake HTTP responses
        self.fake_200_sat_res = MagicMock()
        self.fake_200_sat_res.ok = True
        self.fake_200_sat_res.json.return_value = {
            "countries": "",
            "decayed": None,
            "deployed": None,
            "image": "http://db-dev.satnogs.org/media/satellites/202.png",
            "launched": None,
            "name": "OREFLAT-0",
            "names": "KJ7SAT",
            "norad_cat_id": 99910,
            "operator": "None",
            "status": "alive",
            "telemetries": [],
            "website": "https://www.oresat.org/"
        }

        self.fake_200_tel_res = MagicMock()
        self.fake_200_tel_res.ok = True
        self.fake_200_tel_res.json.return_value = [self.fake_frame]

        fake_req_obj = MagicMock()
        fake_req_obj.method = 'GET'

        self.fake_403_res = MagicMock()
        self.fake_403_res.request = fake_req_obj
        self.fake_403_res.ok = False
        self.fake_403_res.status_code = 403
        self.fake_403_res.url = 'https://db.satnogs.org/api/satellites'

        self.fake_404_res = MagicMock()
        self.fake_404_res.reason = 'Satellite not found!'
        self.fake_404_res.request = fake_req_obj
        self.fake_404_res.ok = False
        self.fake_404_res.status_code = 404
        self.fake_404_res.url = 'https://db.satnogs.org/api/satellites'

    def tearDown(self):
        satnogs.requests = self.old_requests

    def test_request_satellite_parameters(self):
        """Given a valid NORAD ID and SatNOGS token
        When making an HTTP request for satellite metadata
        Then request_satellite should return a valid dict of information
        """
        # Monkeypatch good SatNOGS token
        satnogs.SATNOGS_DB_TOKEN = 'abcd1234'
        os.environ['SATNOGS_DB_TOKEN'] = 'abcd1234'

        # Request parameters
        headers = {
            'Authorization': 'Token abcd1234',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        parameters = {
            'format': 'json',
            'satellite': str(self.norad_id)
        }

        self.mock_requests.get.return_value = self.fake_200_sat_res

        satellite_meta = satnogs.request_satellite(self.norad_id)
        endpoint = f'https://db.satnogs.org/api/satellites/{self.norad_id}'
        satnogs.requests.get.assert_called_with(endpoint,
                                                headers=headers,
                                                params=parameters,
                                                allow_redirects=True)
        self.assertEqual(satellite_meta['name'], 'OREFLAT-0')

    def test_request_satellite_with_no_token(self):
        """Given a valid NORAD ID but no SatNOGS token
        When making an HTTP request for satellite metadata
        Then request_satellite should raise a FailedAPIRequest exception
        """
        # Monkeypatch bad SatNOGS token
        satnogs.SATNOGS_DB_TOKEN = None
        del os.environ['SATNOGS_DB_TOKEN']

        self.mock_requests.get.return_value = self.fake_403_res

        with self.assertRaises(EnvironmentError):
            satnogs.request_satellite(self.norad_id)

    def test_request_satellite_with_bad_norad_id(self):
        """Given an invalid NORAD ID
        When making an HTTP request for satellite metadata
        Then request_satellite should raise a FailedAPIRequest exception
        """
        norad_id = -1

        self.mock_requests.get.return_value = self.fake_404_res
        with self.assertRaises(FailedAPIRequest):
            satnogs.request_satellite(norad_id)

    def test_request_telemetry_parameters(self):
        """Given a valid NORAD ID and SatNOGS token
        When making an HTTP request for telemetry
        Then request_telemetry should return a valid dict of telemetry
        """
        # Monkeypatch good SatNOGS token
        satnogs.SATNOGS_DB_TOKEN = 'abcd1234'
        os.environ['SATNOGS_DB_TOKEN'] = 'abcd1234'

        # Request parameters
        headers = {
            'Authorization': 'Token abcd1234',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        parameters = {
            'format': 'json',
            'satellite': str(self.norad_id)
        }

        self.mock_requests.get.return_value = self.fake_200_tel_res

        telemetry = satnogs.request_telemetry(self.norad_id)
        endpoint = 'https://db.satnogs.org/api/telemetry'
        satnogs.requests.get.assert_called_with(endpoint,
                                                headers=headers,
                                                params=parameters,
                                                allow_redirects=True)
        self.assertEqual(telemetry['observation_id'], 31534)

    def test_request_telemetry_with_no_token(self):
        """Given a valid NORAD ID but no SatNOGS token
        When making an HTTP request for telemetry
        Then request_telemetry should raise a FailedAPIRequest exception
        """
        # Monkeypatch bad SatNOGS token
        satnogs.SATNOGS_DB_TOKEN = None
        del os.environ['SATNOGS_DB_TOKEN']

        self.mock_requests.get.return_value = self.fake_403_res

        with self.assertRaises(EnvironmentError):
            satnogs.request_telemetry(self.norad_id)

    def test_request_telemetry_with_bad_norad_id(self):
        """Given an invalid NORAD ID
        When making an HTTP request for telemetry
        Then request_telemetry should raise a FailedAPIRequest exception
        """
        norad_id = -1

        self.mock_requests.get.return_value = self.fake_404_res
        with self.assertRaises(FailedAPIRequest):
            satnogs.request_telemetry(norad_id)

    def test_decode_valid_telemetry(self):
        """Given a valid hex-string of telemetry
        When calling the OreFlat0 decoder
        Then it should return a dict of correctly decoded data
        """
        expected = {
            "dummy_data": ":KJ7SAT - Test beacon from AX5043 driver. Sun Jan 13 21:38:52 1980\n"
        }
        frame = self.fake_frame.get('frame')
        decoded = satnogs.decode_telemetry_frame(frame)
        self.assertEqual(decoded, expected)

    def test_decode_invalid_telemetry(self):
        """Given an invalid hex-string of telemetry
        When calling the OreFlat0 decoder
        Then it should raise a ValueError
        """
        frame = '00AABBCCDDEEFF'
        with self.assertRaises(ValueError):
            satnogs.decode_telemetry_frame(frame)
