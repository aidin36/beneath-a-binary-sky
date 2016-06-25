# This file is part of Beneath a Binary Sky.
# Copyright (C) 2016, Aidin Gharibnavaz <aidin@aidinhut.com>
#
# Beneach a Binary Sky is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Beneach a Binary Sky is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Beneach a Binary Sky. If not, see
# <http://www.gnu.org/licenses/>.


import unittest
import io
import json

import json_listener


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
        missed_password = {"robot_id": "missing_fields_test",
                           "action": "move"}

        result = self.call_application_func(missed_password)

        self.assertEqual(result["status"], 500)
        self.assertEqual(result["error_code"], "InvalidJSONError")

        missed_password_2 = {"action": "ui"}

        result = self.call_application_func(missed_password)

        self.assertEqual(result["status"], 500)
        self.assertEqual(result["error_code"], "InvalidJSONError")

        missed_robot_id = {"password": "98disdf3",
                           "action": "move"}

        result = self.call_application_func(missed_robot_id)

        self.assertEqual(result["status"], 500)
        self.assertEqual(result["error_code"], "InvalidJSONError")

        missed_action = {"password": "123",
                         "robot_id": "afsfd23"}

        result = self.call_application_func(missed_action)

        self.assertEqual(result["status"], 500)
        self.assertEqual(result["error_code"], "InvalidJSONError")

        missed_all = {}

        result = self.call_application_func(missed_all)

        self.assertEqual(result["status"], 500)
        self.assertEqual(result["error_code"], "InvalidJSONError")


    def test_good_request(self):
        '''An OK request.'''
        request = {"robot_id": "good_request_robot_id",
                   "password": "123",
                   "action": "move"}

        result = self.call_application_func(request)

        # It should pass the JSONListener and stops later by RobotNotFoundError.
        self.assertEqual(result["status"], 500)
        self.assertEqual(result["error_code"], "RobotNotFoundError")

    def test_bad_json(self):
        '''Sends a json in a wrong format.'''
        env = {"REQUEST_METHOD": "POST",
               "wsgi.input": None}

        result = json_listener.application(env, self.fake_start_response)
        result = json.loads(result[0].decode("utf-8"))

        self.assertEqual(result["status"], 500)


        env = {"REQUEST_METHOD": "POST",
               "wsgi.input": '{"action": "ui", "password": "123"}'}

        result = json_listener.application(env, self.fake_start_response)
        result = json.loads(result[0].decode("utf-8"))

        self.assertEqual(result["status"], 500)
