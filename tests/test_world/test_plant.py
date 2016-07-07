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

from database.memcached_database import MemcachedDatabase
from database.exceptions import InvalidLocationError
from world.world import World
from world.exceptions import CannotPlantHereError, LocationIsBlockedError, AlreadyPlantError
from objects.map_square import MapSquare
from objects.map_square_types import MapSquareTypes
from objects.plant import Plant


class TestPlantAction(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        row = [MapSquare(MapSquareTypes.SOIL, (0, 16)),
               MapSquare(MapSquareTypes.ROCK, (1, 16)),
               MapSquare(MapSquareTypes.SAND, (2, 16)),
               MapSquare(MapSquareTypes.WATER, (3, 16)),
               MapSquare(MapSquareTypes.SOIL, (4, 16))]

        database = MemcachedDatabase()
        database.add_square_row(row)

    def tearDown(cls):
        database = MemcachedDatabase()
        database.rollback()

    def test_ok(self):
        '''Tests a good scenario.'''
        world = World()

        new_plant = Plant()
        world.plant(new_plant, (0, 16))

    def test_blocking_location(self):
        '''Tests planting on a blocking location.'''
        world = World()

        new_plant = Plant()
        with self.assertRaises(LocationIsBlockedError):
            world.plant(new_plant, (1, 16))

    def test_non_soil_location(self):
        '''Tests planting on a non-soil location.'''
        world = World()

        new_plant = Plant()
        with self.assertRaises(CannotPlantHereError):
            world.plant(new_plant, (2, 16))

        with self.assertRaises(CannotPlantHereError):
            world.plant(new_plant, (3, 16))

    def test_duplicate(self):
        '''Tests planting twice on a location.'''
        world = World()

        new_plant = Plant()

        world.plant(new_plant, (4, 16))

        MemcachedDatabase().commit()

        with self.assertRaises(AlreadyPlantError):
            world.plant(new_plant, (4, 16))

    def test_bad_location(self):
        '''Tests planting on an invalid location.'''
        world = World()

        new_plant = Plant()
        with self.assertRaises(InvalidLocationError):
            world.plant(new_plant, (1881, 1998))
