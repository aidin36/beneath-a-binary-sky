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
from communicator import Communicator
from listeners.exceptions import InvalidRequestError


def make_error_response(error):
    '''Generates a response for an error.'''
    response = {'status': 500,
                'error_code': type(error).__name__,
                'error_message': str(error)}
    return response

def validate_request(request):
    '''Validates if the request have the required fields.

    @raise InvalidRequestError: If the request is not valid.
    '''
    if 'command' not in request:
        raise InvalidRequestError("`command' key in request is mandatory.")

    if 'password' not in request:
        raise InvalidRequestError("`password' key in request is mandatory.")

    if 'args' not in request:
        raise InvalidRequestError("`args' key should be provided.")

    if not isinstance(request['args'], list):
        raise InvalidRequestError("`args' should be a list. If you don't have any arguments, provide an empty list.")

def handle_request(request):
    try:
        validate_request(request)

        # Communicator is a singleton class.
        communicator = Communicator()

        communicator_result = communicator.execute_command(request["password"],
                                                           request["command"],
                                                           request["args"])
    except Exception as error:
        return make_error_response(error)

    result = {'status': 200,
              'result': communicator_result}

    return result
