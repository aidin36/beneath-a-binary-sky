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

from actions.action import Action
from world.square_iterator import SquareInterator
from world.world import World
from database.memcached_database import MemcachedDatabase


class SenseAction(Action):

    def do_action(self, robot, args):
        '''Gathers and sends information about robot's surrendering.

        @param robot: Instance of `objects.robot.Robot'.
        '''
        world = World()
        database = MemcachedDatabase()

        result = {}
        for square_x, square_y in SquareInterator(robot.get_location(), world.get_size(), max_radios=1):
            square_object = database.get_square(square_x, square_y)

            is_there_a_robot = square_object.get_robot_id() is not None
            is_there_a_plant = square_object.get_plant() is not None

            result["{0},{1}".format(square_x, square_y)] = {"surface_type": square_object.get_type(),
                                                            "robot": is_there_a_robot,
                                                            "plant": is_there_a_plant}

        return result
