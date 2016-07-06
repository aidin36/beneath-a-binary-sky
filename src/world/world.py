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
from database.lock import LockAlreadyAquiredError
from utils.singleton import Singleton
from world.square_iterator import SquareInterator


class World(Singleton):

    def _initialize(self):
        self._database = MemcachedDatabase()
        self._size = (-1, -1)

    def get_size(self):
        '''Returns size of the world.'''
        return self._size

    def add_robot(self, robot, x, y):
        '''Adds a robot to the world.
        It tries to find the nearest empty point to the specified point.

        @param robot: Instance of objects.robot.Robot.
        @param x: Location to try to add the robot. (X)
        @param y: Location to try to add the robot. (Y)
        '''
        for square_x, square_y in SquareInterator((x, y), self._size):
            try:
                square_object = self._database.get_square(square_x, square_y, for_update=True)

                # Checking if something blocked this square.
                if not square_object.is_blocking():
                    robot.set_location(square_x, square_y)
                    self._database.add_robot(robot, square_x, square_y)
                    # Done.
                    return

            except LockAlreadyAquiredError:
                # If this square was locked, go to the next one.
                continue

        raise exceptions.WorldIsFullError("No free location is remained in the world!")

    def move_robot(self, robot, destination):
        '''Moves a robot to the specified location.

        @param destination: A tuple of (x, y)
        '''
        # TODO: Check for the map boundaries.
        # Locking both origin and destination.
        origin = robot.get_location()

        origin_square = self._database.get_square(*origin, for_update=True)
        destination_square = self._database.get_square(*destination, for_update=True)

        origin_square.set_robot_id(None)
        destination_square.set_robot_id(robot.get_id())

        robot.set_location(*destination)

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

                row.append(MapSquare(square_type, (column_number - 1, line_number - 1)))

            self._database.add_square_row(row)

        self._size = (row_length, line_number)
