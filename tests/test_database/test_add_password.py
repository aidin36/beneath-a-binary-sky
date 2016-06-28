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
from database.exceptions import DuplicatedPasswordError, InvalidPasswordError


class TestAddPassword(unittest.TestCase):

    def test_add_and_pop(self):
        '''Adds a password and pops it again.'''
        database = MemcachedDatabase()

        database.add_password("test_add_and_pop_8341")

        database.pop_password("test_add_and_pop_8341")

    def test_duplicate_password(self):
        '''Adds a password twice. Should raise an exception.'''
        database = MemcachedDatabase()

        database.add_password("test_duplicate_8172")

        with self.assertRaises(DuplicatedPasswordError):
            database.add_password("test_duplicate_8172")

    def test_not_exist_password(self):
        '''Tries to pop a password that does not exists. Should raise an exception.'''
        database = MemcachedDatabase()

        with self.assertRaises(InvalidPasswordError):
            database.pop_password("not_exist_password_1873")

    def test_double_pop(self):
        '''Tries to pop a password twice. Should raise an exception.'''
        database = MemcachedDatabase()

        database.add_password("test_double_pop_9864")

        database.pop_password("test_double_pop_9864")

        with self.assertRaises(InvalidPasswordError):
            database.pop_password("test_double_pop_9864")
