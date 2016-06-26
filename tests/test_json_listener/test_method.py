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
import json

import json_listener


class TestMethod(unittest.TestCase):

    def fake_start_response(self, *args, **kwargs):
        pass

    def test_invalid_method(self):
        '''Sends invalid method to the listener.'''
        env = {"REQUEST_METHOD": "GET"}

        json_result = json_listener.application(env, self.fake_start_response)
        result = json.loads(json_result[0].decode('utf-8'))

        self.assertEqual(result['status'], 500)
        self.assertEqual(result['error_code'], 'InvalidHttpMethodError')
