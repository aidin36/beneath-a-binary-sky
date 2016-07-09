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
import time

from database.exceptions import LockAlreadyAquiredError
from database.memcached_database import MemcachedDatabase
from world.world import World
from objects.plant import Plant


class TestObjectUpdaterSquare(unittest.TestCase):
    '''Tests if ObjectUpdater updates the square correctly.'''

    def tearDown(self):
        # Rolling back any remaining changes.
        MemcachedDatabase().rollback()

    def test_one_cycle(self):
        '''Tests if plant updates correctly after one cycle.'''
        plant = Plant()
        world = World()
        database = MemcachedDatabase()

        world.plant(plant, (3, 8))
        database.commit()

        # Sleeping one cycle.
        time.sleep(0.021)

        square = world.get_square((3, 8), for_update=False)

        plant = square.get_plant()

        self.assertEqual(plant.get_age(), 1)
        self.assertEqual(plant.get_water_level(), 90)

    def test_out_of_water(self):
        '''Tests if plant die after running out of water.'''
        plant = Plant()
        world = World()
        database = MemcachedDatabase()

        world.plant(plant, (4, 8))
        database.commit()

        # Waiting for 11 cycles.
        time.sleep(11 * 0.02)

        square = world.get_square((4, 8), for_update=False)

        self.assertIsNone(square.get_plant())

    def test_maximum_age(self):
        '''Tests if plant die after maximum age.'''
        plant = Plant()
        world = World()
        database = MemcachedDatabase()

        world.plant(plant, (5, 8))
        database.commit()

        square = world.get_square((5, 8), for_update=True)
        plant = square.get_plant()
        plant.set_age(40)
        database.commit()

        # Sleeping one cycle.
        time.sleep(0.021)

        square = world.get_square((5, 8), for_update=False)
        self.assertIsNone(square.get_plant())

    def test_no_cycle_passed(self):
        '''Tests if plant not changed if no cycle passed.'''
        world = World()
        database = MemcachedDatabase()
        plant = Plant()
        plant.set_age(2)
        plant.set_water_level(70)

        world.plant(plant, (6, 8))
        database.commit()

        # Waiting just a little.
        time.sleep(0.01)

        square = world.get_square((6, 8), for_update=False)
        received_plant = square.get_plant()

        self.assertEqual(received_plant.get_age(), plant.get_age())
        self.assertEqual(received_plant.get_water_level(), plant.get_water_level())
        self.assertEqual(received_plant.get_last_update(), plant.get_last_update())

    def test_locked_square(self):
        '''Tests updating a locked square.'''
        plant = Plant()
        world = World()
        database = MemcachedDatabase()

        world.plant(plant, (7, 8))
        database.commit()

        # Locking the square.
        world.get_square((7, 8), for_update=True)

        # Sleeping one cycle.
        time.sleep(0.021)

        with self.assertRaises(LockAlreadyAquiredError):
            world.get_square((7, 8), for_update=False)
