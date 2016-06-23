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

import communicator
import utils.logger


def send_error(start_response, error_message):
    '''Sends error to the client.'''
    start_response("500 Error", [])
    error = {'status': 500,
             'error': error_message}
    return [json.dumps(error).encode('utf-8')]


def validate_request(request):
    '''Validates if the request have the required fields.
    
    Returns an error message if the request is invalid,
    returns an empty string otherwise.
    '''
    if 'action' not in request:
        return "`command' key in request is mandatory."

    if 'password' not in request:
        return "`password' key in request is mandatory."

    if request['action'] == 'ui':
        # UI does not have any thing else.
        return ""

    if 'robot_id' not in request:
        return "`robot_id' key in request is mandatory."

    return ""


def application(env, start_response):
    '''A uWSGI application'''

    if env["REQUEST_METHOD"] != "POST":
        return send_error(start_response, "Only POST method allowed")

    json_request = env["wsgi.input"].read()

    try:
        request = json.loads(json_request.decode("utf-8"))
    except Exception as error:
        return send_error(start_response, str(error))

    validation_result = validate_request(request)
    if validation_result != "":
        return send_error(start_response, validation_result)
    
    communicator_result = None
    try:
        if request["action"] == "ui":
            communicator_result = communicator.get_ui_data(request["password"])
        else:
            communicator_result = communicator.do_action(request["robot_id"],
                                                         request["password"],
                                                         request["action"],
                                                         request.get("args"))
    except Exception as error:
        utils.logger.error("Unhandled error: {0}\n{1}".format(error, traceback.format_ex()))
        send_error(start_response, str(error))
    
    result = {'status': 200,
              'result': communicator_result}
    
    start_response('200 OK', [('Content-Type','text/html')])
    return [json.dumps(result).encode('utf-8')]
