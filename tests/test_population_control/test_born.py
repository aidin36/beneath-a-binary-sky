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
from objects.robot import Robot, MAX_ROBOT_NAME
from objects.exceptions import LongRobotNameError
from population.population_control import PopulationControl
from database.memcached_database import MemcachedDatabase
from database.exceptions import InvalidPasswordError


class TestBorn(unittest.TestCase):

    def test_ok(self):
        '''Tests a good scenario.'''
        population_control = PopulationControl()
        database = MemcachedDatabase()

        database.add_password("iujeh87UYh6512ewQ")

        robot_info = population_control.execute_command("iujeh87UYh6512ewQ", "born", [None, "RDaniel"])
        database.commit()

        gotted_robot = database.get_robot(robot_info['robot_id'])

        self.assertEqual(gotted_robot.get_name(), "RDaniel")

    def test_wrong_password(self):
        '''Tests borning a robot with wrong password.'''
        population_control = PopulationControl()

        with self.assertRaises(InvalidPasswordError):
            population_control.execute_command("wrong_pass_1273", "born", [])

    def test_bad_parent_id(self):
        '''Tests with an invalid parent ID.'''
        population_control = PopulationControl()

        with self.assertRaises(InvalidArgumentsError):
            population_control.execute_command("123", "born", [1334])

        with self.assertRaises(InvalidArgumentsError):
            population_control.execute_command("123", "born", [b"some bytes"])

    def test_with_parent(self):
        '''Tests borning a robot with a parent.'''
        population_control = PopulationControl()
        database = MemcachedDatabase()

        database.add_password("oijdnnh76153WEd")
        robot = Robot("test_with_parent_18873", "123")
        database.add_robot(robot, (14, 1))
        database.commit()

        population_control.execute_command("oijdnnh76153WEd", "born", ["test_with_parent_18873", "My Child"])

        database.rollback()

    def test_bad_name(self):
        '''Tries to born a robot with an invalid name. Should be fail.'''
        population_control = PopulationControl()
        database = MemcachedDatabase()

        database.add_password("OIkdj981HJDJHcnm_1")
        database.add_password("OIkdj981HJDJHcnm_2")
        database.add_password("OIkdj981HJDJHcnm_3")
        database.add_password("OIkdj981HJDJHcnm_4")
        database.commit()

        long_name = "n" * (MAX_ROBOT_NAME + 1)
        with self.assertRaises(LongRobotNameError):
            population_control.execute_command("OIkdj981HJDJHcnm_1", "born", [None, long_name])
        database.rollback()

        with self.assertRaises(LongRobotNameError):
            population_control.execute_command("OIkdj981HJDJHcnm_2", "born", [None, None])
        database.rollback()

        with self.assertRaises(LongRobotNameError):
            population_control.execute_command("OIkdj981HJDJHcnm_3", "born", [None, b"some bytes"])
        database.rollback()

        with self.assertRaises(LongRobotNameError):
            population_control.execute_command("OIkdj981HJDJHcnm_4", "born", [None, database])
        database.rollback()
