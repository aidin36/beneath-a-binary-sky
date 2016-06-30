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
from database.memcached_database import MemcachedDatabase


class TestInfoAction(unittest.TestCase):

    def test_blind_point(self):
        '''Gets information of a point, but don't care about the result.'''
        new_robot = Robot("1873yudhNCbueio", "ueijdnchiop")
        new_robot.set_location(9, 7)
        MemcachedDatabase().add_robot(new_robot, 9, 7)

        action_manager = ActionManager()
        info = action_manager.do_action(new_robot.get_password(), "info", [new_robot.get_id()])

        self.assertEqual(len(info), 9)

    def test_specific_point(self):
        '''Gets information of a specific point, and check its result.'''
        new_robot = Robot("oie982736hhjf", "lo098173635")
        new_robot.set_location(9, 4)
        MemcachedDatabase().add_robot(new_robot, 9, 4)

        action_manager = ActionManager()
        info = action_manager.do_action(new_robot.get_password(), "info", [new_robot.get_id()])

        self.assertEqual(len(info), 9)
        self.assertEqual(info["9,4"], {"surface_type": MapSquareTypes.SOIL,
                                       "robot": True,
                                       "plant": False})
        self.assertEqual(info["9,3"], {"surface_type": MapSquareTypes.WATER,
                                       "robot": False,
                                       "plant": False})
        self.assertEqual(info["10,5"], {"surface_type": MapSquareTypes.SOIL,
                                        "robot": False,
                                        "plant": False})
        self.assertEqual(info["8,4"], {"surface_type": MapSquareTypes.SOIL,
                                       "robot": False,
                                       "plant": False})

    def test_corner(self):
        '''Tests getting a corner of the map.'''
        new_robot = Robot("0981kdjieu871", "oie987163")
        new_robot.set_location(0, 1)
        MemcachedDatabase().add_robot(new_robot, 0, 1)

        action_manager = ActionManager()
        info = action_manager.do_action(new_robot.get_password(), "info", [new_robot.get_id()])

        self.assertEqual(len(info), 6)
