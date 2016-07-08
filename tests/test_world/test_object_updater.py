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
from world.world import World
from objects.robot import Robot


class TestObjectUpdater(unittest.TestCase):

    def tearDown(self):
        # Rolling back any remaning things.
        MemcachedDatabase().rollback()

    def test_out_of_life_robot(self):
        '''Tests when a robot ran out of life.'''
        database = MemcachedDatabase()
        world = World()

        robot = Robot("test_out_of_life_robot_9022", "123")
        robot.set_life(0)

        world.add_robot(robot, 0, 9)
        database.commit()

        received_robot = database.get_robot("test_out_of_life_robot_9022", for_update=False)
        self.assertFalse(received_robot.get_alive())

        square = world.get_square((0, 9))
        self.assertIsNone(square.get_robot_id())

    def test_out_of_energy_robot(self):
        '''Tests when a robot ran out of energy.'''
        database = MemcachedDatabase()
        world = World()

        robot = Robot("test_out_of_energy_robot_18773", "123")
        robot.set_energy(0)

        world.add_robot(robot, 1, 9)
        database.commit()

        got_robot = database.get_robot("test_out_of_energy_robot_18773", for_update=False)
        self.assertFalse(got_robot.get_alive())

        square = world.get_square((1, 9))
        self.assertIsNone(square.get_robot_id())
