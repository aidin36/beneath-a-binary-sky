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
from database.exceptions import LockAlreadyAquiredError
from database.memcached_database import MemcachedDatabase
from objects.robot import Robot
from population.exceptions import NotEnoughHonorError
from population.population_control import PopulationControl
from world.world import World
from utils.configs import Configs


class TestGiveBirth(unittest.TestCase):

    ROBOT_ID = "test_give_birth_1889"

    @classmethod
    def setUpClass(cls):
        # Creating a robot that all the tests will use.
        database = MemcachedDatabase()
        world = World()
        robot = Robot(TestGiveBirth.ROBOT_ID, "123")
        world.add_robot(robot, (0, 14))
        database.commit()

    def test_ok(self):
        '''Tests a valid situation.'''
        population_control = PopulationControl()
        database = MemcachedDatabase()
        configs = Configs()

        robot = database.get_robot(TestGiveBirth.ROBOT_ID, for_update=True)
        robot.set_honor(configs.get_robots_birth_required_honor() + 1)
        database.commit()

        new_password = population_control.execute_command("123", "give_birth", [TestGiveBirth.ROBOT_ID])
        database.commit()

        updated_robot = database.get_robot(TestGiveBirth.ROBOT_ID, for_update=False)

        self.assertEqual(updated_robot.get_honor(), 1)
        self.assertTrue(isinstance(new_password, str))
        self.assertEqual(len(new_password), 16)

    def test_invalid_args(self):
        '''Tests the method with some invalid arguments.'''
        population_control = PopulationControl()

        with self.assertRaises(InvalidArgumentsError):
            population_control.execute_command("123", "give_birth", [None])

        with self.assertRaises(InvalidArgumentsError):
            population_control.execute_command("123", "give_birth", [TestGiveBirth.ROBOT_ID, "Extra arg"])

        with self.assertRaises(InvalidArgumentsError):
            population_control.execute_command(None, "give_birth", [TestGiveBirth.ROBOT_ID])

    def test_locked_robot(self):
        '''Tests with a locked robot.'''
        population_control = PopulationControl()
        database = MemcachedDatabase()
        database.get_robot(TestGiveBirth.ROBOT_ID, for_update=True)

        with self.assertRaises(LockAlreadyAquiredError):
            population_control.execute_command("123", "give_birth", [TestGiveBirth.ROBOT_ID])

        database.rollback()

    def test_not_enough_honor(self):
        '''Tests a robot with few honors, trying to give birth.'''
        population_control = PopulationControl()
        database = MemcachedDatabase()
        configs = Configs()

        robot = database.get_robot(TestGiveBirth.ROBOT_ID, for_update=True)
        robot.set_honor(configs.get_robots_birth_required_honor() - 1)
        database.commit()

        with self.assertRaises(NotEnoughHonorError):
            population_control.execute_command("123", "give_birth", [TestGiveBirth.ROBOT_ID])

        database.rollback()
