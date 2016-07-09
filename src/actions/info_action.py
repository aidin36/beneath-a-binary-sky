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
from actions.exceptions import InvalidArgumentsError
from world.world import World
from utils.configs import Configs


class InfoAction(Action):

    def __init__(self):
        self._world = World()
        self._configs = Configs()

    def do_action(self, robot, args):
        '''Returns information about the world..

        @param robot: Instance of `objects.robot.Robot'.
        '''
        if len(args) != 1:
            raise InvalidArgumentsError("`info' takes no arguments.")

        return {'world_size': self._world.get_size(),
                'plant_max_age': self._configs.get_plant_max_age(),
                'plant_matured_age': self._configs.get_plant_matured_age()}
