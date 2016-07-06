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

from database.memcached_database import MemcachedDatabase
from objects.robot import Robot
from database.lock import LockAlreadyAquiredError


class TestGetRobot(unittest.TestCase):

    def test_for_update(self):
        '''Tests of for_update flag works correctly.'''
        database = MemcachedDatabase()

        robot_id = "test_for_update_18762"
        robot = Robot(robot_id, "123")
        database.add_robot(robot, 10, 0)
        database.commit()

        new_robot = database.get_robot(robot_id, for_update=True)

        # Testing lock
        with self.assertRaises(LockAlreadyAquiredError):
            database.get_robot(robot_id, for_update=True)

        # Testing commit.
        new_robot.set_alive(False)

        # It shouldn't be changed yet.
        new_robot_2 = database.get_robot(robot_id)
        self.assertNotEqual(new_robot.get_alive(), new_robot_2.get_alive())

        # Actually committing changes.
        database.commit()
        new_robot_2 = database.get_robot(robot_id)
        self.assertEqual(new_robot.get_alive(), new_robot_2.get_alive())

        # Lock should be freed.
        database.get_robot(robot_id, for_update=True)
        database.rollback()

    def test_rollback(self):
        '''Tests if changes rolls back correctly.'''
        database = MemcachedDatabase()

        robot_id = "test_rollback_18098"
        robot = Robot(robot_id, "123")
        database.add_robot(robot, 11, 0)
        database.commit()

        new_robot = database.get_robot(robot_id, for_update=True)
        new_robot.set_alive(False)

        database.rollback()
        database.commit()

        new_robot_2 = database.get_robot(robot_id)
        self.assertNotEqual(new_robot.get_alive(), new_robot_2.get_alive())
