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

import world.exceptions as exceptions
from objects.map_square import MapSquare
from database.memcached_database import MemcachedDatabase
from database.lock import Lock
from utils.singleton import Singleton

class World(Singleton):

    def _initialize(self):
        self._database = MemcachedDatabase()
        self._size = (-1, -1)

    def get_size(self):
        '''Returns size of the world.'''
        return self._size

    def add_robot(self, robot, x, y):
        '''Adds a robot to the world.

        @param robot: Instance of objects.robot.Robot.
        @param x: Location of the robot (X)
        @param y: Location of the robot (Y)
        '''
        # TODO: Check for blocking objects.
        with Lock("{0},{1}".format(x, y)):
            self._database.add_robot(robot, x, y)

    def load_from_file(self, file_path):
        '''Loads a world from the specified file.'''
        with open(file_path, 'r') as world_file:
            file_lines = world_file.readlines()

        row_length = None
        line_number = 0

        for line in file_lines:
            line = line.replace('\r', '').replace('\n', '')

            if line.startswith("#") or line.isspace():
                continue

            line_number += 1

            # Keeping length of the first line, so we can validate that all
            # the lines have same length.
            if row_length is None:
                row_length = len(line)

            if len(line) != row_length:
                raise exceptions.InvalidWorldFileError("Length of line {0} is invalid.".format(line_number))

            row = []
            column_number = 0
            for square_type in line:
                column_number += 1
                square_type = int(square_type)

                if square_type not in (0, 1, 2, 3):
                    raise exceptions.InvalidWorldFileError(
                        "Found invalid square in line {0} column {1}.".format(line_number, column_number))

                row.append(MapSquare(square_type))

            self._database.add_square_row(row, line_number - 1)

        self._size = (row_length, line_number)
