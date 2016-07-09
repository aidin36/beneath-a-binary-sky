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

from objects.map_square_types import MapSquareTypes
from actions.action_manager import ActionManager
from objects.robot import Robot
from objects.plant import Plant
from database.memcached_database import MemcachedDatabase
from world.world import World


class TestInfoAction(unittest.TestCase):

    def test_blind_point(self):
        '''Gets information of a point, but don't care about the result.'''
        database = MemcachedDatabase()
        new_robot = Robot("1873yudhNCbueio", "ueijdnchiop")
        new_robot.set_location(9, 7)

        database.add_robot(new_robot, 9, 7)
        database.commit()

        action_manager = ActionManager()
        info = action_manager.do_action(new_robot.get_password(), "sense", [new_robot.get_id()])

        self.assertEqual(len(info), 9)

    def test_specific_point(self):
        '''Gets information of a specific point, and check its result.'''
        database = MemcachedDatabase()
        new_robot = Robot("oie982736hhjf", "lo098173635")
        new_robot.set_location(9, 4)

        database.add_robot(new_robot, 9, 4)
        database.commit()

        action_manager = ActionManager()
        info = action_manager.do_action(new_robot.get_password(), "sense", [new_robot.get_id()])

        self.assertEqual(len(info), 9)
        self.assertEqual(info["9,4"], {"surface_type": MapSquareTypes.SOIL,
                                       "robot": True,
                                       "plant": None})
        self.assertEqual(info["9,3"], {"surface_type": MapSquareTypes.WATER,
                                       "robot": False,
                                       "plant": None})
        self.assertEqual(info["10,5"], {"surface_type": MapSquareTypes.SOIL,
                                        "robot": False,
                                        "plant": None})
        self.assertEqual(info["8,4"], {"surface_type": MapSquareTypes.SOIL,
                                       "robot": False,
                                       "plant": None})

    def test_corner(self):
        '''Tests getting a corner of the map.'''
        database = MemcachedDatabase()
        new_robot = Robot("0981kdjieu871", "oie987163")
        new_robot.set_location(0, 1)

        database.add_robot(new_robot, 0, 1)
        database.commit()

        action_manager = ActionManager()
        info = action_manager.do_action(new_robot.get_password(), "sense", [new_robot.get_id()])

        self.assertEqual(len(info), 6)

    def test_plant(self):
        '''Tests sensing a plant.'''
        world = World()
        database = MemcachedDatabase()

        new_robot = Robot("poeiekfm98871", "123")

        plant = Plant()
        plant.set_age(12)
        plant.set_water_level(60)

        world.plant(plant, (11, 4))
        database.commit()
        world.add_robot(new_robot, 11, 4)
        database.commit()

        action_manager = ActionManager()
        info = action_manager.do_action(new_robot.get_password(), "sense", [new_robot.get_id()])

        self.assertEqual(info["11,4"], {"surface_type": MapSquareTypes.SOIL,
                                        "robot": True,
                                        "plant": {"age": 12,
                                                  "water_level": 60,
                                                  "matured": True}})
