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

from actions.exceptions import InvalidArgumentsError
from actions.info_action import InfoAction
from objects.robot import Robot
from world.world import World
from utils.configs import Configs
from database.memcached_database import MemcachedDatabase

class TestInfoAction(unittest.TestCase):

    def test_info(self):
        '''Test received information.'''
        action = InfoAction()
        world = World()
        configs = Configs()
        robot = Robot("test_info_action_1293", "123")

        info = action.do_action(robot, [robot.get_id()])

        self.assertEqual(info['world_size'], world.get_size())
        self.assertEqual(info['plant_max_age'], configs.get_plant_max_age())
        self.assertEqual(info['plant_matured_age'], configs.get_plant_matured_age())
        self.assertEqual(info['action_delay'], configs.get_robots_actions_delay())

    def test_bad_arguments(self):
        '''Calls the action with invalid arguments.'''
        action = InfoAction()
        database = MemcachedDatabase()
        robot = Robot("test_info_action_1293", "123")

        with self.assertRaises(InvalidArgumentsError):
            action.do_action(robot, [robot.get_id(), None])
        database.rollback()

        with self.assertRaises(InvalidArgumentsError):
            action.do_action(robot, [robot.get_id(), "", "09"])
        database.rollback()

        with self.assertRaises(InvalidArgumentsError):
            action.do_action(robot, [robot.get_id(), []])
