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

import traceback
import json

import listeners.listener as listener
from listeners.exceptions import InvalidHttpMethodError
from utils.logger import Logger


def application(env, start_response):
    '''A uWSGI application'''

    try:
        if env["REQUEST_METHOD"] != "POST":
            raise InvalidHttpMethodError("Only POST method allowed")

        json_request = env["wsgi.input"].read()

        request = json.loads(json_request.decode("utf-8"))

        result = listener.handle_request(request)

        start_response('200 OK', [('Content-Type', 'text/html')])
        return [json.dumps(result).encode('utf-8')]

    except Exception as error:
        Logger().error("JSON Listener: {0}\n{1}".format(error, traceback.format_exc()))
        start_response("500 Error", [])
        return [str(error)]
