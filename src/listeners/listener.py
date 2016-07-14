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
import os

from communicator import Communicator
from listeners.exceptions import InvalidRequestError
from database.memcached_database import MemcachedDatabase
from utils.exceptions import BinarySkyException
from utils.logger import Logger
from utils.configs import Configs


def initialize_process(): # pragma: no cover - This will be mocked in the tests an never runs.
    '''Initializes the newly forked process'''
    config_file_path = os.environ.get("BINARY_SKY_CONFIG_FILE")
    logging_config_path = os.environ.get("BINARY_SKY_LOGGING_FILE")

    Configs().load_configs(config_file_path)
    Logger().load_configs(logging_config_path)
    MemcachedDatabase().initialize()


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
    except BinarySkyException as error:
        return make_error_response(error)
    except Exception as error:
        # Logging exceptions that are not one of ours.
        Logger().error("System error: {0}\n{1}".format(error, traceback.format_exc()))
        return make_error_response(error)

    result = {'status': 200,
              'result': communicator_result}

    return result
