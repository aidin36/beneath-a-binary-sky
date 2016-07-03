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

from population.population_control import PopulationControl
from database.memcached_database import MemcachedDatabase
from database.exceptions import InvalidPasswordError


class TestBorn(unittest.TestCase):

    def test_ok(self):
        '''Tests a good scenario.'''
        population_control = PopulationControl()
        database = MemcachedDatabase()

        database.add_password("iujeh87UYh6512ewQ")

        robot_info = population_control.execute_command("iujeh87UYh6512ewQ", "born", [])
        database.commit()

        database.get_robot(robot_info['robot_id'])

    def test_wrong_password(self):
        '''Tests borning a robot with wrong password.'''
        population_control = PopulationControl()

        with self.assertRaises(InvalidPasswordError):
            population_control.execute_command("wrong_pass_1273", "born", [])

    # TODO: Add this test when world completed.
#    def test_with_parent(self):
