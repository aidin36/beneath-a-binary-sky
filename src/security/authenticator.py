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

import database
from database.exception import DatabaseException


class AuthenticationFailedError(Exception):
    '''Raises if a robot could not be authenticated.'''


class Authenticator:

    def authenticate_robot(self, robot_id, password):
        '''Authenticate the robot access and its password.'''
        correct_password = database.db.get_robot_password(robot_id)

        if password == correct_password:
            return

        raise AuthenticationFailedError("Wrong password for Robot {0}".format(robot_id))