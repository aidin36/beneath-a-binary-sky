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

from database.memcached_connection import MemcachedConnection
from database.exception import DatabaseException


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

    def add_robot(self, robot_object, x, y):
        '''Adds the new robot object to the specified position.'''
        mc_connection = MemcachedConnection().get_connection()

        result = mc_connection.add(robot_object.get_id(), robot_object)

        if not result:
            error_message = "Robot {0} is already exists, or there's something wrong with the database."
            raise CannotAddRobotError(error_message.format(robot_object.get_id()))

    def get_robot(self, robot_id):
        '''Gets the robot object with the specified ID from the database.

        @raise RobotNotFoundError: When no robot found with this ID.
        '''
        mc_connection = MemcachedConnection().get_connection()

        result = mc_connection.get(robot_id)

        if result is None:
            raise RobotNotFoundError("Robot {0} not found.".format(robot_id))

        return result

    def get_ui_password(self):
        '''
        '''

    def set_ui_password(self):
        '''
        '''
