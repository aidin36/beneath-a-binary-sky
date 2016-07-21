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

import msgpack
import http.client

from exceptions import HTTPRequestFailedError, BornError


class Communicator:
    '''This class handles the communication between the robot (client) and
    the server (world).
    '''

    @classmethod
    def configure(cls, host, port):
        '''
        @param host: IP of the server to connect to.
        @param port: Port to connect to.
        '''
        cls._robot_id = None
        cls._password = None
        cls._connection = http.client.HTTPSConnection(host, port=port)

    @classmethod
    def born(cls, password):
        '''Borns the robot.'''
        request = {'command': 'born',
                   'password': password,
                   'args': []}
        response = cls._send_http_request(request)

        if response['status'] != 200:
            raise BornError("{0}:{1}".format(response['error_code'], response['error_message']))

        cls._robot_id = response['result']['robot_id']
        cls._password = response['result']['password']

    @classmethod
    def send_action(cls, action_key, args):
        '''Sends the specified action to the server.

        @param action_key: Str
        @param password: Str
        @param args: List
        '''
        if args is None:
            args = []

        # Robot ID should always be send as the first argument.
        args.insert(0, cls._robot_id)

        request = {'command': action_key,
                   'password': cls._password,
                   'args': args}

        return cls._send_http_request(request)

    @classmethod
    def _send_http_request(cls, request):
        '''Serializes the request and sends it to the server.'''
        cls._connection.request("POST", "/msgpack", msgpack.packb(request))

        http_response = cls._connection.getresponse()

        if http_response.getcode() != 200:
            raise HTTPRequestFailedError(http_response.read())

        return msgpack.unpackb(http_response.read(), encoding='utf-8')
