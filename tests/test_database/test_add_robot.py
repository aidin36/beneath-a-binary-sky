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

import unittest

from database.memcached_database import MemcachedDatabase
from database.memcached_database import CannotAddRobotError
from objects.robot import Robot


class TestAddRobot(unittest.TestCase):

    def test_simple_add(self):
        '''Test adding a single robot to database.'''
        database = MemcachedDatabase()

        new_robot = Robot("test_simple_add_", "123")

        # No exception should be raise.
        database.add_robot(new_robot, 0, 0)

    def test_duplicate_add(self):
        '''Adding two robots with same ID. Should be failed.'''
        database = MemcachedDatabase()

        new_robot = Robot("test_duplicate_add_", "123")
        database.add_robot(new_robot, 1, 1)

        robot2 = Robot("test_duplicate_add_", "123")
        with self.assertRaises(CannotAddRobotError):
            database.add_robot(robot2, 1, 2)
