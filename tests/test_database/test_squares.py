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
from database.exceptions import DatabaseException, InvalidLocationError, LockAlreadyAquiredError
from objects.map_square import MapSquare
from objects.map_square_types import MapSquareTypes


class TestSquares(unittest.TestCase):

    def test_ok(self):
        '''Tests an OK scenario.'''
        database = MemcachedDatabase()

        row = [MapSquare(MapSquareTypes.SOIL, (0, 999)),
               MapSquare(MapSquareTypes.WATER, (1, 999)),
               MapSquare(MapSquareTypes.ROCK, (2, 999)),
               MapSquare(MapSquareTypes.SAND, (3, 999))]

        database.add_square_row(row)

        self.assertEqual(database.get_square(0, 999).get_type(), MapSquareTypes.SOIL)
        self.assertEqual(database.get_square(1, 999).get_type(), MapSquareTypes.WATER)
        self.assertEqual(database.get_square(2, 999).get_type(), MapSquareTypes.ROCK)
        self.assertEqual(database.get_square(3, 999).get_type(), MapSquareTypes.SAND)

    def test_duplicate_add(self):
        '''Tests adding two squares at the same location. Should raise exception.'''
        database = MemcachedDatabase()

        row = [MapSquare(MapSquareTypes.SOIL, (0, 998))]

        database.add_square_row(row)

        with self.assertRaises(DatabaseException):
            database.add_square_row(row)

    def test_not_exists_square(self):
        '''Tests getting a square that does not exists.'''
        database = MemcachedDatabase()

        with self.assertRaises(InvalidLocationError):
            database.get_square(19873, 1736)

    def test_for_update(self):
        '''Tests for_update flag of get_square method.'''
        database = MemcachedDatabase()

        square = database.get_square(6, 1, for_update=True)

        # Testing the lock.
        with self.assertRaises(LockAlreadyAquiredError):
            database.get_square(6, 1, for_update=True)

        # Testing commit.
        square.set_robot_id("ujhqi981762yhdg67")

        # It shouldn't be changed yet.
        new_square = database.get_square(6, 1)
        self.assertNotEqual(square.get_robot_id(), new_square.get_robot_id())

        # Committing changes.
        database.commit()
        new_square = database.get_square(6, 1)
        self.assertEqual(square.get_robot_id(), new_square.get_robot_id())

        # Lock should be freed.
        new_square = database.get_square(6, 1, for_update=True)
        database.rollback()

    def test_rollback(self):
        '''Tests if database rolls back the changes correctly.'''
        database = MemcachedDatabase()

        square = database.get_square(6, 2, for_update=True)
        square.set_robot_id("iuwuyehdmn990198283")

        database.rollback()
        database.commit()

        new_square = database.get_square(6, 2)
        self.assertNotEqual(square.get_robot_id(), new_square.get_robot_id())
