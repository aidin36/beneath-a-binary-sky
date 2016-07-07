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

from actions.water_action import WaterAction
from actions.exceptions import RobotHaveNoWaterError, InvalidArgumentsError
from objects.robot import Robot
from objects.plant import Plant
from world.world import World
from database.memcached_database import MemcachedDatabase
from database.exceptions import LockAlreadyAquiredError


class TestWaterAction(unittest.TestCase):

    def test_water_level(self):
        '''Tests if water level increases after watering.'''
        database = MemcachedDatabase()
        world = World()

        robot = Robot("198.1287.fkdfjei", "123")
        robot.set_location(5, 0)
        robot.set_has_water(True)

        plant = Plant()
        plant.set_water_level(30)

        world.plant(plant, (5, 0))

        database.commit()

        action = WaterAction()
        action.do_action(robot, ["198.1287.fkdfjei"])

        database.commit()

        updated_square = world.get_square((5, 0))
        plant = updated_square.get_plant()

        self.assertEqual(plant.get_water_level(), 100)
        self.assertFalse(robot.get_has_water())

    def test_locked_square(self):
        '''Tests with a already-locked square.'''
        database = MemcachedDatabase()
        robot = Robot("oi981872yuweu.9887", "123")
        robot.set_location(5, 0)
        robot.set_has_water(True)

        database.get_square(5, 0, for_update=True)

        action = WaterAction()

        with self.assertRaises(LockAlreadyAquiredError):
            action.do_action(robot, ["oi981872yuweu.9887"])

        # Freeing lock.
        database.rollback()

    def test_no_plant_square(self):
        '''Tests watering a square without any plant.'''
        database = MemcachedDatabase()

        robot = Robot("098kk.ski87.99", "123")
        robot.set_location(6, 0)
        robot.set_has_water(True)

        action = WaterAction()

        action.do_action(robot, ["098kk.ski87.99"])

        self.assertFalse(robot.get_has_water())

        database.rollback()

    def test_have_no_water(self):
        '''Tests if a robot has water.'''
        robot = Robot("1223.9887.099", "123")
        robot.set_location(6, 0)
        robot.set_has_water(False)

        action = WaterAction()

        with self.assertRaises(RobotHaveNoWaterError):
            action.do_action(robot, ["1223.9887.099"])

    def test_bad_arguments(self):
        '''Tests passing invalid arguments.'''
        robot = Robot("AweeRf567Qw", "123")

        action = WaterAction()

        with self.assertRaises(InvalidArgumentsError):
            action.do_action(robot, ["AweeRf567Qw", None])

        with self.assertRaises(InvalidArgumentsError):
            action.do_action(robot, ["AweeRf567Qw", "", 3345])

        with self.assertRaises(InvalidArgumentsError):
            action.do_action(robot, ["AweeRf567Qw", []])
