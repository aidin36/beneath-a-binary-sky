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

import json
import sys
import unittest
import unittest.mock

# Mocking uwsgi module, since we're not running listener module as a UWSGI application.
uwsgidecorators_mock = unittest.mock.MagicMock()
uwsgidecorators_mock.postfork.return_value = None
sys.modules['uwsgidecorators'] = uwsgidecorators_mock

from listeners import json_listener


class TestMethod(unittest.TestCase):

    def fake_start_response(self, *args, **kwargs):
        pass

    def test_invalid_method(self):
        '''Sends invalid method to the listener.'''
        env = {"REQUEST_METHOD": "GET"}

        result = json_listener.application(env, self.fake_start_response)
        self.assertEqual(result[0], "Only POST method allowed")
