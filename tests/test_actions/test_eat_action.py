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

from utils.configs import Configs
from actions.action_manager import ActionManager
from actions.exceptions import InvalidArgumentsError, NoPlantToEat
from world.world import World
from objects.robot import Robot
from objects.plant import Plant
from database.memcached_database import MemcachedDatabase


class TestEatAction(unittest.TestCase):

    ROBOT_ID = "test_eat_action_1928"
    LOCATION = (13, 10)

    @classmethod
    def setUpClass(cls):
        # Addin a robot to the world. All the tests would use this robot.
        robot = Robot(cls.ROBOT_ID, "123")
        world = World()

        world.add_robot(robot, cls.LOCATION)

        database = MemcachedDatabase()
        database.commit()

    def test_eating_matured(self):
        '''Tests when robot eat a matured plant.'''
        world = World()
        database = MemcachedDatabase()
        action_manager = ActionManager()
        plant = Plant()
        plant.set_age(Configs().get_plant_matured_age() + 1)

        world.plant(plant, TestEatAction.LOCATION)
        database.commit()

        robot = database.get_robot(TestEatAction.ROBOT_ID, for_update=True)
        robot.set_energy(10)
        database.commit()

        action_manager.do_action("123", "eat", [TestEatAction.ROBOT_ID])
        database.commit()

        updated_robot = database.get_robot(TestEatAction.ROBOT_ID)
        self.assertGreater(updated_robot.get_energy(), robot.get_energy())

    def test_eating_not_matured(self):
        '''Tests when robot eat a non matured plant.'''
        world = World()
        database = MemcachedDatabase()
        action_manager = ActionManager()
        plant = Plant()
        plant.set_age(1)

        world.plant(plant, TestEatAction.LOCATION)
        database.commit()

        robot = database.get_robot(TestEatAction.ROBOT_ID, for_update=True)
        robot.set_energy(10)
        database.commit()

        action_manager.do_action("123", "eat", [TestEatAction.ROBOT_ID])
        database.commit()

        updated_robot = database.get_robot(TestEatAction.ROBOT_ID)
        self.assertEqual(updated_robot.get_energy(), robot.get_energy() - 1)

    def test_bad_argument(self):
        '''Tests when sending bad arguments to the action.'''
        action_manager = ActionManager()
        database = MemcachedDatabase()

        with self.assertRaises(InvalidArgumentsError):
            action_manager.do_action("123", "eat", [TestEatAction.ROBOT_ID, None])
        database.rollback()

        with self.assertRaises(InvalidArgumentsError):
            action_manager.do_action("123", "eat", [TestEatAction.ROBOT_ID, "", 9])
        database.rollback()

    def test_no_plant(self):
        '''Tests when there's no plant to eat.'''
        action_manager = ActionManager()
        database = MemcachedDatabase()

        with self.assertRaises(NoPlantToEat):
            action_manager.do_action("123", "eat", [TestEatAction.ROBOT_ID])
        database.rollback()
