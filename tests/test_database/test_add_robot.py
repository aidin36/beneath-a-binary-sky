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

import unittest
import unittest.mock

from database.memcached_database import MemcachedDatabase
from database.exceptions import CannotAddObjectError
from database.exceptions import CouldNotSetValueBecauseOfConcurrencyError
from database.exceptions import RobotNotFoundError, InvalidLocationError
from database.memcached_connection import MemcachedConnection
from objects.robot import Robot


class TestAddRobot(unittest.TestCase):

    def test_simple_add(self):
        '''Test adding a single robot to database.'''
        database = MemcachedDatabase()

        new_robot = Robot("test_simple_add_", "123")

        # No exception should be raise.
        database.add_robot(new_robot, 0, 0)
        database.commit()

        gotted_robot = database.get_robot("test_simple_add_")

        self.assertEqual(gotted_robot.get_id(), new_robot.get_id())
        self.assertEqual(gotted_robot.get_alive(), new_robot.get_alive())
        self.assertEqual(gotted_robot.get_password(), new_robot.get_password())

    def test_duplicate_add(self):
        '''Adding two robots with same ID. Should be failed.'''
        database = MemcachedDatabase()

        new_robot = Robot("test_duplicate_add_", "123")
        database.add_robot(new_robot, 1, 1)
        database.commit()

        robot2 = Robot("test_duplicate_add_", "123")
        with self.assertRaises(CannotAddObjectError):
            database.add_robot(robot2, 1, 2)
            database.commit()

    def test_concurrent_add_failure(self):
        '''Tests the behavior of Database class, when concurrent add fails.'''

        # Mocking `cas' method, making it always return False.
        def mocked_cas(*args):
            return False
        mc_connection = MemcachedConnection().get_connection()
        original_cas = mc_connection.cas
        mc_connection.cas = unittest.mock.Mock(side_effect=mocked_cas)

        try:
            new_robot = Robot("test_concurrent_add_failure_9865", "123")
            database = MemcachedDatabase()

            with self.assertRaises(CouldNotSetValueBecauseOfConcurrencyError):
                database.add_robot(new_robot, 1, 1)
                database.commit()

        finally:
            # Setting back the original cas method.
            mc_connection.cas = original_cas

        # Checking to see added robot is clearly rolled back.
        self.assertFalse(mc_connection.get(new_robot.get_id()))

    def test_rollback(self):
        '''Tests if calling rollback works correctly.'''
        database = MemcachedDatabase()

        new_robot = Robot("test_rollback_87162", "123")
        database.add_robot(new_robot, 1, 1)

        database.rollback()
        database.commit()

        with self.assertRaises(RobotNotFoundError):
            database.get_robot("test_rollback_87162")

    def test_invalid_location(self):
        '''Tests if database checks for invalid locations.'''
        database = MemcachedDatabase()

        new_robot = Robot("test_invalid_location_19887", "123")

        with self.assertRaises(InvalidLocationError):
            database.add_robot(new_robot, 91872, 16652)
            database.commit()
