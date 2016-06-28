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

from database.memcached_database import MemcachedDatabase


class AuthenticationFailedError(Exception):
    '''Raises if a robot could not be authenticated.'''


class Authenticator:

    def __init__(self):
        self._database = MemcachedDatabase()

    def authenticate_robot(self, robot_object, password):
        '''Authenticate the robot access and its password.'''

        # Ensuring that password is a string.
        if not isinstance(password, str):
            raise AuthenticationFailedError("Wrong password for Robot {0}".format(robot_object.get_id()))

        if password != robot_object.get_password():
            raise AuthenticationFailedError("Wrong password for Robot {0}".format(robot_object.get_id()))

        if not robot_object.get_alive():
            raise AuthenticationFailedError("Robot {0} is dead!".format(robot_object.get_id()))

    def authenticate_new_robot(self, password):
        '''Authenticate if this password is valid for a new robot to join the game
        (e.g. born).
        It remove the password from the database. i.e. the password can use for
        only one born.

        @raise InvalidPasswordError: If password wasn't valid.
        '''
        self._database.pop_password(password)
