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

import math


class SquareInterator:
    '''Iterates squares around a point.

    Note that first returning point is the center point itself.

    example usage:
        for x, y in SquareIterator((4, 3), (100, 100))
    '''

    ITERATION_DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def __init__(self, center_point, map_size, max_radios=None):
        '''
        @param center_point: Point to iterate around.
        @param map_size: Size of the current map (world).
        @keyword max_radios: If provided, it iterates to this maximum distance
            from the center. For example, if center is on Y 3, and max_radios is
            2, it will goes up to Y 5.
        '''
        self._center_x = center_point[0]
        self._center_y = center_point[1]
        self._map_size_x = map_size[0]
        self._map_size_y = map_size[1]
        self._max_raios = max_radios

    def __iter__(self):
        return next(self)

    def __next__(self):
        # First point is the center itself.
        yield (self._center_x, self._center_y)

        # The walking algorithm:
        # It iterates points around the center, in a shape of square.
        # First, it finds the upper left corner of the square. Then, it moves to the right.
        # After reaching the right edge, it moves down. Then, left, then, up.
        # After that, it increase the size of the square's side by one, and iterates again.

        # How many squares to walk in each row? e.g. Square's side size.
        length = 0

        while True:
            square_found = False
            length += 2
            corner_x = self._center_x - math.floor(length / 2)
            corner_y = self._center_y - math.floor(length / 2)

            current_x = corner_x
            current_y = corner_y

            for direction in SquareInterator.ITERATION_DIRECTIONS:
                for i in range(length):
                    current_x += direction[0]
                    current_y += direction[1]

                    if (current_x < 0 or current_x > self._map_size_x - 1 or
                        current_y < 0 or current_y > self._map_size_y - 1):
                        # Out of map.
                        continue

                    square_found = True
                    yield (current_x, current_y)

            if not square_found:
                # If nothing found after a complete loop (e.g. we iterate all possible points.)
                raise StopIteration()

            if self._max_raios is not None and (length / 2) >= self._max_raios:
                # We iterated to the maximum requested radios.
                raise StopIteration()
