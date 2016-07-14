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

from utils.id_generator import IDGenerator


class TestIDGenerator(unittest.TestCase):

    def test_id_serial(self):
        '''Tests if the serial of the ID increases.'''
        id_generator = IDGenerator()

        first_id = id_generator.get_robot_id()
        second_id = id_generator.get_robot_id()

        self.assertEqual(int(first_id.split('.')[2]) + 1,
                         int(second_id.split('.')[2]))
