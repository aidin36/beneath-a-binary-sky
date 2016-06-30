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

from objects.map_square_types import MapSquareTypes


class MapSquare:

    def __init__(self, type):
        self._type = type
        self._robot_id = None
        self._plant = None

    def get_type(self):
        '''Gets the type of this square. It would be one of MapSqareTypes.'''
        return self._type

    def set_robot_id(self, robot_id):
        '''Sets the ID of robot which stands on this square.'''
        self._robot_id = robot_id

    def get_robot_id(self):
        '''Returns ID of the robot which stands on this square.'''
        return self._robot_id

    def set_plant(self, plant):
        '''Sets the plant that lives on this square.'''
        self._plant = plant

    def get_plant(self):
        '''Returns the plant that lives on this square.'''
        return self._plant

    def is_blocking(self):
        '''Returns True if a robot cannot walk into this square. Returns false otherwise.'''
        return (self._type == MapSquareTypes.ROCK or self._robot_id is not None)
