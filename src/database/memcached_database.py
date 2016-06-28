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

import time

from database.memcached_connection import MemcachedConnection
import database.exceptions as exceptions


PASSWORD_PREFIX = "P_"


class MemcachedDatabase:

    def initialize(self):
        '''Initializes the database by setting required key-values.'''
        mc_connection = MemcachedConnection().get_connection()

        mc_connection.add("all_robots", [])

    def add_robot(self, robot_object, x, y):
        '''Adds the new robot object to the specified position.

        @raise CannotAddRobotError
        @raise CouldNotSetValueBecauseOfCuncurrency
        '''
        mc_connection = MemcachedConnection().get_connection()

        result = mc_connection.add(robot_object.get_id(), robot_object)

        if not result:
            error_message = "Robot {0} is already exists, or there's something wrong with the database."
            raise exceptions.CannotAddRobotError(error_message.format(robot_object.get_id()))

        try:
            self._add_robot_to_all_list(robot_object.get_id())
        except Exception:
            # Rolling back previous add.
            mc_connection.delete(robot_object.get_id())
            raise

    def get_robot(self, robot_id):
        '''Gets the robot object with the specified ID from the database.

        @raise RobotNotFoundError: When no robot found with this ID.
        '''
        mc_connection = MemcachedConnection().get_connection()

        result = mc_connection.get(robot_id)

        if result is None:
            raise exceptions.RobotNotFoundError("Robot {0} not found.".format(robot_id))

        return result

    def get_all_robot_ids(self):
        '''Gets a list of all robot IDs exists in the database.'''
        mc_connection = MemcachedConnection().get_connection()

        return mc_connection.get("all_robots")

    def add_password(self, password):
        '''Adds the specified password to the database.'''
        mc_connection = MemcachedConnection().get_connection()

        result = mc_connection.add("{0}{1}".format(PASSWORD_PREFIX, password), 1)

        if not result:
            raise exceptions.DuplicatedPasswordError()

    def pop_password(self, password):
        '''Removes a password from database.

        This operation is atomic, no concurrency will happen.

        @raise InvalidPasswordError: If password not found.
        '''
        mc_connection = MemcachedConnection().get_connection()

        password_key = "{0}{1}".format(PASSWORD_PREFIX, password)

        result = mc_connection.delete(password_key)

        if not result:
            raise exceptions.InvalidPasswordError()

    def _add_robot_to_all_list(self, robot_id):
        '''Adds a robot to the list of all robot IDs.'''
        mc_connection = MemcachedConnection().get_connection()

        # Trying seven times to set the `all_robots' object, and checking for concurrency optimistically.
        for i in range(7):
            all_robots, cas_key = mc_connection.gets("all_robots")

            all_robots.append(robot_id)

            result = mc_connection.cas("all_robots", all_robots, cas_key)

            if result:
                return

            # Waiting 20 miliseconds before next try.
            time.sleep(0.02)

        # We couldn't set it, after seven tries.
        raise exceptions.CouldNotSetValueBecauseOfCuncurrency("Could not update `all_robots' object.")
