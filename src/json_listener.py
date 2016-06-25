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

import traceback
import json

from communicator import Communicator
import utils.logger


class InvalidJSONError(Exception):
    '''Raises if received JSON is not valid. i.e. it dose not have required fields.'''

class InvalidHttpMethodError(Exception):
    '''Raises if the HTTP Method is not acceptable.'''


def send_error(start_response, error):
    '''Sends error to the client.'''
    start_response("500 Error", [])
    error = {'status': 500,
             'error_code': type(error).__name__,
             'error_message': str(error)}
    return [json.dumps(error).encode('utf-8')]


def validate_request(request):
    '''Validates if the request have the required fields.
    
    @raise InvalidJSONError: If the request is not valid.
    '''
    if 'action' not in request:
        raise InvalidJSONError("`command' key in request is mandatory.")

    if 'password' not in request:
        InvalidJSONError("`password' key in request is mandatory.")

    if request['action'] == 'ui':
        # UI does not have any thing else.
        return

    if 'robot_id' not in request:
        InvalidJSONError("`robot_id' key in request is mandatory.")


def application(env, start_response):
    '''A uWSGI application'''

    try:
        if env["REQUEST_METHOD"] != "POST":
            raise InvalidHttpMethodError("Only POST method allowed")

        json_request = env["wsgi.input"].read()

        request = json.loads(json_request.decode("utf-8"))

        validate_request(request)

        # Communicator is a singleton class.
        communicator = Communicator()

        if request["action"] == "ui":
            communicator_result = communicator.get_ui_data(request["password"])
        else:
            communicator_result = communicator.do_action(request["robot_id"],
                                                         request["password"],
                                                         request["action"],
                                                         request.get("args"))
    except Exception as error:
        utils.logger.error("JSON Listener: {0}\n{1}".format(error, traceback.format_exc()))
        return send_error(start_response, error)

    result = {'status': 200,
              'result': communicator_result}
    
    start_response('200 OK', [('Content-Type','text/html')])
    return [json.dumps(result).encode('utf-8')]
