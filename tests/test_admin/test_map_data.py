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
from admin.admin_handler import AdminHandler
from communicator import Communicator
from security.authenticator import AuthenticationFailedError
from database.memcached_database import MemcachedDatabase
from objects.robot import Robot
from objects.plant import Plant
from objects.map_square_types import MapSquareTypes


class TestMapData(unittest.TestCase):

    def test_bad_password(self):
        admin_handler = AdminHandler()

        with self.assertRaises(AuthenticationFailedError):
            admin_handler.execute_command("Amdn387DipeNcmaq2", "map_data", ["0,0"])

        with self.assertRaises(InvalidArgumentsError):
            admin_handler.execute_command(None, "map_data", ["0,0"])

        with self.assertRaises(InvalidArgumentsError):
            admin_handler.execute_command(object(), "map_data", ["0,0"])

        with self.assertRaises(InvalidArgumentsError):
            admin_handler.execute_command(1445, "map_data", ["0,0"])

    def test_getting_data(self):
        robot = Robot("13329.12900.12213", "123", name="HappyBot")
        robot.set_energy(124)
        robot.set_honor(7)
        robot.set_life(3)
        robot.set_has_water(True)

        plant = Plant()
        plant.set_age(64)
        plant.set_water_level(98)

        database = MemcachedDatabase()
        database.add_robot(robot, (6, 11))
        square = database.get_square((5, 11), for_update=True)
        square.set_plant(plant)
        database.commit()

        expected_result = {"5,11": {"surface_type": MapSquareTypes.SOIL,
                                    "plant": {"water_level": 98,
                                              "matured": True,
                                              "age": 64},
                                    "robot": None},
                           "6,11": {"surface_type": MapSquareTypes.SOIL,
                                    "plant": None,
                                    "robot": {"name": "HappyBot",
                                              "has_water": True,
                                              "energy": 124,
                                              "life": 3,
                                              "honor": 7}},
                           "6,2": {"surface_type": MapSquareTypes.ROCK,
                                   "robot": None,
                                   "plant": None}
                           }

        communicator = Communicator()
        result = communicator.execute_command("NhdEr32Qcmp0Iue3", "map_data", expected_result.keys())

        self.assertCountEqual(result, expected_result)
        for expected_key, expected_value in expected_result.items():
            self.assertDictEqual(result[expected_key], expected_value)
