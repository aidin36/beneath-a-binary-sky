# This file is part of Beneath a Binary Sky.
# Copyright (C) 2016, Aidin Gharibnavaz <aidin@aidinhut.com>
#
# Beneath a Binary Sky is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Beneath a Binary Sky is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Beneath a Binary Sky. If not, see
# <http://www.gnu.org/licenses/>.


import io
import sys
import json
import unittest
import unittest.mock

# Mocking uwsgi module, since we're not running listener module as a UWSGI application.
uwsgidecorators_mock = unittest.mock.MagicMock()
uwsgidecorators_mock.postfork.return_value = None
sys.modules['uwsgidecorators'] = uwsgidecorators_mock

from listeners import json_listener


class TestReqiest(unittest.TestCase):

    def fake_start_response(self, *args, **kwargs):
        pass

    def call_application_func(self, request):
        '''Helper method for calling `application' function of
        `json_listener' module.
        '''
        json_request = json.dumps(request)
        request_object = io.BytesIO(json_request.encode("utf-8"))

        env = {"REQUEST_METHOD": "POST",
               "wsgi.input": request_object}

        result = json_listener.application(env, self.fake_start_response)
        return json.loads(result[0].decode("utf-8"))

    def test_missing_fields(self):
        '''Sends a request which some of its fields are missed.'''
        missed_password = {"command": "move",
                           "args": ["jfnfdhdfieop"]}

        result = self.call_application_func(missed_password)

        self.assertEqual(result["status"], 500)
        self.assertEqual(result["error_code"], "InvalidRequestError")

        missed_command = {"password": "123",
                          "args": []}

        result = self.call_application_func(missed_command)

        self.assertEqual(result["status"], 500)
        self.assertEqual(result["error_code"], "InvalidRequestError")

        missed_args = {"password": "123",
                       "command": "status"}

        result = self.call_application_func(missed_args)

        self.assertEqual(result["status"], 500)
        self.assertEqual(result["error_code"], "InvalidRequestError")

        missed_all = {}

        result = self.call_application_func(missed_all)

        self.assertEqual(result["status"], 500)
        self.assertEqual(result["error_code"], "InvalidRequestError")

    def test_bad_args(self):
        '''Sends bad args.'''
        request = {"password": "123",
                   "command": "move",
                   "args": None}

        result = self.call_application_func(request)

        self.assertEqual(result["status"], 500)
        self.assertEqual(result["error_code"], "InvalidRequestError")

        request = {"password": "123",
                   "command": "move",
                   "args": ""}

        result = self.call_application_func(request)

        self.assertEqual(result["status"], 500)
        self.assertEqual(result["error_code"], "InvalidRequestError")

    def test_good_request(self):
        '''An OK request.'''
        request = {"password": "123",
                   "command": "status",
                   "args": ["good_request_robot_id_09187"]}

        result = self.call_application_func(request)

        # It should pass the JSONListener and stops later by RobotNotFoundError.
        self.assertEqual(result["status"], 500)
        self.assertEqual(result["error_code"], "RobotNotFoundError")

    def test_bad_json(self):
        '''Sends a json in a wrong format.'''
        env = {"REQUEST_METHOD": "POST",
               "wsgi.input": None}

        result = json_listener.application(env, self.fake_start_response)
        self.assertEqual(result[0], "'NoneType' object has no attribute 'read'")

        env = {"REQUEST_METHOD": "POST",
               "wsgi.input": '{"action": "ui", "password": "123"}'}

        result = json_listener.application(env, self.fake_start_response)
        self.assertEqual(result[0], "'str' object has no attribute 'read'")
