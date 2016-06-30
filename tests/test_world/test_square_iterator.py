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
from world.square_iterator import SquareInterator


class TestSquareIterator(unittest.TestCase):

    def test_against_predefined_result(self):
        '''Tests the iterator against hard-coded result.'''

        expected_result = [(1, 1),
                           (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (0, 1), (0, 0),
                           (3, 0), (3, 1), (3, 2), (3, 3), (2, 3), (1, 3), (0, 3)]

        counter = 0
        for point in SquareInterator((1, 1), (4, 4)):
            self.assertEqual(expected_result[counter], point)
            counter += 1
