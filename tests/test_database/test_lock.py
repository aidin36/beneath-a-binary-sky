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

from database.lock import Lock, LockAlreadyAquiredError


class TestLock(unittest.TestCase):

    def test_double_lock(self):
        '''Takes a lock two times. Should be fail.'''
        l1 = Lock("test_double_lock")
        l1.aquire()

        with self.assertRaises(LockAlreadyAquiredError):
            l2 = Lock("test_double_lock")
            l2.aquire()

    def test_release(self):
        '''Tests wether lock releasing work.'''
        l1 = Lock("test_release_lock")
        l1.aquire()
        l1.release()

        l2 = Lock("test_release_lock")
        l1.aquire()
        l1.release()

    def test_with_block(self):
        '''Tests if lock works inside a with block.'''
        with Lock("test_with_block_lock"):
            with self.assertRaises(LockAlreadyAquiredError):
                l = Lock("test_with_block_lock")
                l.aquire()

        l2 = Lock("test_with_block_lock")
        l2.aquire()
