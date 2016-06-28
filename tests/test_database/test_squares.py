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
from database.exceptions import DatabaseException, InvalidLocationError
from objects.map_square import MapSquare
from objects.map_square_types import MapSquareTypes


class TestSquares(unittest.TestCase):

    def test_ok(self):
        '''Tests an OK scenario.'''
        database = MemcachedDatabase()

        row = [MapSquare(MapSquareTypes.SOIL),
               MapSquare(MapSquareTypes.WATER),
               MapSquare(MapSquareTypes.ROCK),
               MapSquare(MapSquareTypes.SAND)]

        database.add_square_row(row, 999)

        self.assertEqual(database.get_square(0, 999).get_type(), MapSquareTypes.SOIL)
        self.assertEqual(database.get_square(1, 999).get_type(), MapSquareTypes.WATER)
        self.assertEqual(database.get_square(2, 999).get_type(), MapSquareTypes.ROCK)
        self.assertEqual(database.get_square(3, 999).get_type(), MapSquareTypes.SAND)

    def test_duplicate_add(self):
        '''Tests adding two squares at the same location. Should raise exception.'''
        database = MemcachedDatabase()

        row = [MapSquare(MapSquareTypes.SOIL)]

        database.add_square_row(row, 998)

        with self.assertRaises(DatabaseException):
            database.add_square_row(row, 998)

    def test_not_exists_square(self):
        '''Tests getting a square that does not exists.'''
        database = MemcachedDatabase()

        with self.assertRaises(InvalidLocationError):
            database.get_square(19873, 1736)
