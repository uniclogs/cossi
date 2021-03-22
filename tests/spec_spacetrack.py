import os
import unittest
from unittest.mock import MagicMock
import cosi.spacetrack as spacetrack


class SpaceTrack_Spec(unittest.TestCase):
    def setUp(self):
        self.norad_id = 46922  # Bobcat-1

        # Monkeypatch the request library with a mock
        self.mock_requests = MagicMock()
        self.old_requests = spacetrack.requests
        spacetrack.requests = self.mock_requests

        # Create Fake TLE
        self.tle_json = [{'TLE_LINE0': '0 BOBCAT-1', 'TLE_LINE1': '1 46922U 98067RS  20322.34274700  .00063753  00000-0  10864-2 0  9994', 'TLE_LINE2': '2 46922  51.6465 310.5391 0000331 221.0790 139.2081 15.50762596  1867'}]
        self.tle = ('1 46922U 98067RS  20322.34274700  .00063753  00000-0  10864-2 0  9994',
                    '2 46922  51.6465 310.5391 0000331 221.0790 139.2081 15.50762596  1867')

        # Create fake HTTP responses
        self.fake_200_res = MagicMock()
        self.fake_200_res.ok = True
        self.fake_200_res.status_code = 200
        self.fake_200_res.url = 'https://www.space-track.org'
        self.fake_200_res.json.return_value = []

        fake_req_obj = MagicMock()
        fake_req_obj.method = 'GET'

        self.fake_403_res = MagicMock()
        self.fake_403_res.request = fake_req_obj
        self.fake_403_res.ok = False
        self.fake_403_res.status_code = 403
        self.fake_403_res.url = 'https://www.space-track.org'

        # Create fake request.Session
        self.fake_session = MagicMock()
        self.fake_session.get.json.return_value = self.tle_json
        self.fake_session.post.return_value = self.fake_200_res

    def tearDown(self):
        spacetrack.requests = self.old_requests

    def test_login_spacetrack_no_username(self):
        """Given no SpaceTrack username
        When calling create_spacetrack_session
        Then it should raise an EnvironmentError
        """
        # Monkeypatch no SpaceTrack username
        spacetrack.SPACETRACK_USERNAME = None
        if(os.environ.get('SPACETRACK_USERNAME')):
            del os.environ['SPACETRACK_USERNAME']

        self.mock_requests.post.return_value = self.fake_403_res

        with self.assertRaises(EnvironmentError):
            spacetrack.create_spacetrack_session()

    def test_login_spacetrack_no_password(self):
        """Given no SpaceTrack password
        When calling create_spacetrack_session
        Then it should raise an EnvironmentError
        """
        # Monkeypatch no SpaceTrack username
        spacetrack.SPACETRACK_PASSWORD = None
        if(os.environ.get('SPACETRACK_PASSWORD')):
            del os.environ['SPACETRACK_PASSWORD']

        self.mock_requests.post.return_value = self.fake_403_res

        with self.assertRaises(EnvironmentError):
            spacetrack.create_spacetrack_session()

    def test_login_valid(self):
        """Given valid login credentials
        When calling create_spacetrack_session
        Then it should return an authenticated session
        """
        # Monkeypatch valid credentials
        spacetrack.SPACETRACK_USERNAME = 'andrew'
        os.environ['SPACETRACK_USERNAME'] = 'andrew'
        spacetrack.SPACETRACK_PASSWORD = 'password'
        os.environ['SPACETRACK_PASSWORD'] = 'password'

        self.mock_requests.Session.return_value = self.fake_session

        session = spacetrack.create_spacetrack_session()
        self.assertIsNotNone(session)

    @unittest.skip('TODO: Mock the session response')
    def test_request_tle(self):
        """Given a valid NORAD ID
        When calling request_tle
        Then it should return a vaild tuple of the latest TLE
        """
        # Monkeypatch valid credentials
        spacetrack.SPACETRACK_USERNAME = 'andrew'
        os.environ['SPACETRACK_USERNAME'] = 'andrew'
        spacetrack.SPACETRACK_PASSWORD = 'password'
        os.environ['SPACETRACK_PASSWORD'] = 'password'

        tle = spacetrack.request_tle(self.norad_id)
        # self.assertEqual(tle, self.tle)
