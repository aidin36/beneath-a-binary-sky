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

import pylibmc

from database.memcached_connection import MemcachedConnection
from database.exception import DatabaseException


# These abbrevations used to reduce the size of keys, thus
# reducing the size of database and overhead of communicating with it.
ROBOT_PASSWORD_PREFIX = "RP-"


class CannotAddRobotError(DatabaseException):
    '''Raises when there is a problem for adding a robot to the database.
    Common causes:
        Robot ID is already exists.
        Memcached is not started.
        Memory is full.
    '''

class RobotNotFoundError(DatabaseException):
    '''Raises if a robot cannot be found on the database.'''


class MemcachedDatabase:

    def add_robot_password(self, robot_id, password):
        '''Adds a robot's password to the database.
        
        @raise CannotAddRobotError: If robot exists, or any
            errors happen.
        '''
        mc_connection = MemcachedConnection().get_connection()

        result = mc_connection.add("{0}{1}".format(ROBOT_PASSWORD_PREFIX, robot_id),
                                   password)

        if not result:
            raise CannotAddRobotError("Robot ID is already exists, or there's something wrong with the database.")

    def get_robot_password(self, robot_id):
        '''Returns password of the specified robot ID.
        
        @raise RobotNotFoundError: Raises if nothing found with
            the specified robot ID.
        '''
        mc_connection = MemcachedConnection().get_connection()

        result = mc_connection.get("{0}{1}".format(ROBOT_PASSWORD_PREFIX, robot_id))
        
        if result is None:
            raise RobotNotFoundError("Robot {0} not found.".format(robot_id))

        return result

    def get_ui_password(self):
        '''
        '''

    def set_ui_password(self):
        '''
        '''