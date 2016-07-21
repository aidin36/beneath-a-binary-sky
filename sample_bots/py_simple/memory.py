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

from helpers.square_types import SquareTypes


class Memory:

    def __init__(self):
        self._map = {}
        self._last_saw_soil = None
        self._last_saw_water = None
        self._world_info = {}
        self._first_plant_location = None
        self._second_plant_location = None
        self._third_plant_location = None

    def update_squares(self, squares):
        '''Updates the specified squares in the memory.

        @param squares: A dictionary which maps a square ID to
            the description of that square. This is what receives
            from the world server.
        '''
        print("Memorizing these locations:", squares)
        self._map.update(squares)

        for location, square in squares.items():
            # We save the location of the soil and water the robot last seen.
            # So we can know what is the nearest soil or water.
            # Though it's not a very good algorithm, but it works for this
            # simple robot.
            if square['surface_type'] == SquareTypes.SOIL:
                self._last_saw_soil = location
            if square['surface_type'] == SquareTypes.WATER:
                self._last_saw_water = location

    def get_square(self, location):
        return self._map.get(location)

    def get_nearest_soil(self):
        '''Returns the nearest soil to the robot.'''
        return self._last_saw_soil

    def get_nearest_water(self):
        '''Returns the nearest water to the robot.'''
        return self._last_saw_water

    def memorize_world_info(self, info):
        self._world_info = info

    def get_birth_required_honor(self):
        return self._world_info['birth_required_honor']

    def store_first_plant_location(self, location):
        self._first_plant_location = location

    def get_first_plant_location(self):
        return self._first_plant_location

    def store_second_plant_location(self, location):
        self._second_plant_location = location

    def get_second_plant_location(self):
        return self._second_plant_location
