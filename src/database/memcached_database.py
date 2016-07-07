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

from utils.singleton import Singleton
from utils.configs import Configs
from database.memcached_connection import MemcachedConnection
from database.transaction import Transaction
import database.exceptions as exceptions


PASSWORD_PREFIX = "P_"


class MemcachedDatabase(Singleton):

    def _initialize(self):
        self._current_transaction = None

    def initialize(self):
        '''Initializes the database by setting required key-values.'''
        mc = MemcachedConnection()
        mc.config_connection(Configs().get_database_port())

        mc_connection = mc.get_connection()
        mc_connection.add("all_robots", [])

    def get_lock(self, lock_key):
        '''Gets a lock on database.
        It will be release automatically when transaction commit/rollback.
        '''
        transaction = self._get_transaction()

        transaction.get_lock(lock_key)

    def commit(self):
        '''Commits all changes to database.'''
        transaction = self._get_transaction()

        try:
            transaction.commit()
        finally:
            self._reset_transaction()

    def rollback(self):
        '''Rollbacks all the changes so far.
        After calling this, you should no-longer use objects you received from database.
        '''
        transaction = self._get_transaction()

        try:
            transaction.rollback()
        finally:
            self._reset_transaction()

    def add_square_row(self, row):
        '''Adds a row of squares to the map.

        @note: It's not transactional. It changes the database at realtime.

        @param row: A list of MapSqare.
        '''
        mc_connection = MemcachedConnection().get_connection()

        for square in row:
            result = mc_connection.add(square.get_id(), square)
            if not result:
                raise exceptions.DatabaseException("A square is already exists in location {0}!".format(square.get_id()))

    def get_square(self, x, y, for_update=False):
        '''Gets a map square.

        @param for_update: If you want to update this square (store its
            changes back to the database) you should set this flag.
            Note that it automatically updates the changes when
            `commit' method calls.

        @raise InvalidLocationError
        @raise LockAlreadyAquiredError
        '''
        square_id = "{0},{1}".format(x, y)

        if for_update:
            self.get_lock(square_id)

        mc_connection = MemcachedConnection().get_connection()

        result = mc_connection.get(square_id)

        if result is None:
            raise exceptions.InvalidLocationError("Location {0},{1} is not valid.".format(x, y))

        if for_update:
            transaction = self._get_transaction()
            transaction.store_object(result)

        return result

    def add_robot(self, robot_object, x, y):
        '''Adds the new robot object to the specified position.

        @raise CannotAddRobotError
        @raise CouldNotSetValueBecauseOfConcurrencyError
        '''
        transaction = self._get_transaction()

        transaction.add_object(robot_object)

        # Note that if any errors happen afterward, changes to `all_list' would not be rolled
        # back. Because it have a very little chance that `add_robot_to_location' fails, unless
        # there's something really wrong. And also if this happen, nothing will goes wrong,
        # because later we checked for the validity of `all_robots' list.
        self._add_robot_to_all_list(robot_object.get_id())

        self._add_robot_to_location(robot_object.get_id(), x, y)

    def get_robot(self, robot_id, for_update=False):
        '''Gets the robot object with the specified ID from the database.

        @param robot_id: ID of the robot to get from database.
        @param for_update: If you want to update this robot (store its
            changes back to the database) you should set this flag.
            Note that it automatically updates the changes when
            `commit' method calls.

        @raise RobotNotFoundError: When no robot found with this ID.
        @raise LockAlreadyAquiredError
        '''
        if for_update:
            self.get_lock(robot_id)

        mc_connection = MemcachedConnection().get_connection()

        result = mc_connection.get(robot_id)

        if result is None:
            raise exceptions.RobotNotFoundError("Robot {0} not found.".format(robot_id))

        if for_update:
            transaction = self._get_transaction()
            transaction.store_object(result)

        return result

    def get_all_robot_ids(self):
        '''Gets a list of all robot IDs exists in the database.

        @note There's a little chance that some of the robots in this list
        no longer exists.
        '''
        mc_connection = MemcachedConnection().get_connection()

        return mc_connection.get("all_robots")

    def add_password(self, password):
        '''Adds the specified password to the database.

        @note: It's not transactional. It will add the password directly to the database.
        '''
        mc_connection = MemcachedConnection().get_connection()

        result = mc_connection.add("{0}{1}".format(PASSWORD_PREFIX, password), 1)

        if not result:
            raise exceptions.DuplicatedPasswordError()

    def pop_password(self, password):
        '''Removes a password from database.

        This operation is atomic, no concurrency will happen.

        @note: It's not transactional. It will pop the password directly
            from the database.

        @raise InvalidPasswordError: If password not found.
        '''
        mc_connection = MemcachedConnection().get_connection()

        password_key = "{0}{1}".format(PASSWORD_PREFIX, password)

        result = mc_connection.delete(password_key)

        if not result:
            raise exceptions.InvalidPasswordError()

    def _get_transaction(self):
        '''Gets the current transaction.'''
        if self._current_transaction is None:
            self._current_transaction = Transaction()

        return self._current_transaction

    def _reset_transaction(self):
        '''Resets the transaction, so next time, a new transaction will be started.'''
        self._current_transaction = None

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
        raise exceptions.CouldNotSetValueBecauseOfConcurrencyError("Could not update `all_robots' object.")

    def _add_robot_to_location(self, robot_id, x, y):
        '''Adds the specified robot ID to the specified location on the map.'''
        mc_connection = MemcachedConnection().get_connection()

        location_id = "{0},{1}".format(x, y)
        map_square = mc_connection.get(location_id)

        if map_square is None:
            # This exception should never happen!
            raise exceptions.InvalidLocationError("MapSquare object on {0},{1} not found!".format(x, y))

        map_square.set_robot_id(robot_id)

        transaction = self._get_transaction()
        transaction.store_object(map_square)
