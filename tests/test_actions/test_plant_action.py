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

from actions.plant_action import PlantAction
from actions.exceptions import InvalidArgumentsError
from objects.robot import Robot
from objects.map_square import MapSquare
from objects.map_square_types import MapSquareTypes
from database.memcached_database import MemcachedDatabase


class TestPlantAction(unittest.TestCase):

    def test_ok(self):
        '''Tests a good scenario.'''
        row = [MapSquare(MapSquareTypes.SOIL, (0, 17))]
        database = MemcachedDatabase()
        database.add_square_row(row)

        plant_action = PlantAction()

        robot = Robot("18873.182873.1123", "123")
        robot.set_location((0, 17))

        plant_action.do_action(robot, ["18873.182873.1123"])

    def test_bad_args(self):
        '''Tests the action with invalid arguments.'''
        plant_action = PlantAction()

        robot = Robot("918872.18711.0092", "123")

        with self.assertRaises(InvalidArgumentsError):
            plant_action.do_action(robot, ["918872.18711.0092", None])

