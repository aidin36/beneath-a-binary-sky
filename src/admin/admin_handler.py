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

from actions.exceptions import InvalidArgumentsError
from security.authenticator import Authenticator
from database.memcached_database import MemcachedDatabase


class AdminHandler:
    '''Handles the requests related to GUI.'''

    def __init__(self):
        self._authenticator = Authenticator()
        self._database = MemcachedDatabase()

    def execute_command(self, password, command, args):
        '''Executes the specified command.'''
        if not isinstance(password, str):
            raise InvalidArgumentsError("Expected {0} as password, found {1}.".format(type(str), type(password)))

        self._authenticator.authenticate_admin(password)

        if command == "map_data":
            return self._get_map_data(args)

    def _get_map_data(self, args):
        '''Returns the information about the world's map.

        @args: Should be a list of locations. Each location is a string
            in the form of "x,y".
        '''
        squares = self._database.get_squares(args)

        result = {}
        for location, square in squares.items():
            robot_id = square.get_robot_id()
            if robot_id is not None:
                robot = self._database.get_robot(robot_id)
                robot_info = {'name': robot.get_name(),
                              'has_water': robot.get_has_water(),
                              'energy': robot.get_energy(),
                              'life': robot.get_life(),
                              'honor': robot.get_honor()}
            else:
                robot_info = None

            plant = square.get_plant()
            if plant is not None:
                plant_info = {'water_level': plant.get_water_level(),
                              'matured': plant.is_matured(),
                              'age': plant.get_age()}
            else:
                plant_info = None

            result[location] = {'surface_type': square.get_type(),
                                'plant': plant_info,
                                'robot': robot_info}

        return result
