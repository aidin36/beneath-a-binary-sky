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

from objects.robot import Robot
from world.world import World
from database.memcached_database import MemcachedDatabase
from database.exceptions import CannotAddRobotError


class AddRobotTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(AddRobotTest, self).__init__(*args, **kwargs)

        self._world = World()

    def test_duplicate(self):
        '''Tests adding duplicate robot.'''
        robot = Robot("world_duplicate_robot_8722", "123")

        self._world.add_robot(robot, 5, 1)

        robot_2 = Robot("world_duplicate_robot_8722", "1236")
        with self.assertRaises(CannotAddRobotError):
            self._world.add_robot(robot_2, 5, 2)

    def test_ok(self):
        '''Adds a good robot object to the world.'''
        robot = Robot("world_ok_robot_38364", "123")

        self._world.add_robot(robot, 5, 0)

        database = MemcachedDatabase()
        gotted_robot = database.get_robot(robot.get_id())

        self.assertEqual(gotted_robot.get_alive(), robot.get_alive())

        all_robots = database.get_all_robot_ids()
        self.assertIn(robot.get_id(), all_robots)

    # TODO: Add this test after completion of the world class.
#    def test_blocked_location(self):
