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

from objects.map_square import MapSquare
from objects.map_square_types import MapSquareTypes
from database.memcached_database import MemcachedDatabase
from actions.pick_water import PickWaterAction
from actions.exceptions import NoWaterError, InvalidArgumentsError
from objects.robot import Robot


class TestPickWater(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        row = [MapSquare(MapSquareTypes.WATER, (0, 18)),
               MapSquare(MapSquareTypes.SOIL, (1, 18)),
               MapSquare(MapSquareTypes.SAND, (2, 18))]

        database = MemcachedDatabase()
        database.add_square_row(row)

    def tearDown(cls):
        database = MemcachedDatabase()
        database.rollback()

    def test_ok(self):
        '''Tests a good scenario.'''
        action = PickWaterAction()
        robot = Robot("19882ukfdjfhuoIE", "123")
        robot.set_location(0, 18)

        action.do_action(robot, ["19882ukfdjfhuoIE"])

        self.assertTrue(robot.get_have_water())

    def test_non_water_square(self):
        '''Tests trying to pick water from a dry location.'''
        action = PickWaterAction()
        robot = Robot("19882ukfdjfhuoIE", "123")

        robot.set_location(1, 18)
        with self.assertRaises(NoWaterError):
            action.do_action(robot, ["19882ukfdjfhuoIE"])

        robot.set_location(2, 18)
        with self.assertRaises(NoWaterError):
            action.do_action(robot, ["19882ukfdjfhuoIE"])

    def test_bad_arguments(self):
        '''Tests invalid arguments.'''
        action = PickWaterAction()
        robot = Robot("19882ukfdjfhuoIE", "123")
        robot.set_location(0, 18)

        with self.assertRaises(InvalidArgumentsError):
            action.do_action(robot, [])

        with self.assertRaises(InvalidArgumentsError):
            action.do_action(robot, ["19882ukfdjfhuoIE", ""])
