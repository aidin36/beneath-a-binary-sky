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

import time

from actions.action import Action
from actions.exceptions import InvalidArgumentsError, NoPlantToEat
from database.exceptions import LockAlreadyAquiredError
from world.world import World
from utils.configs import Configs


class EatAction(Action):

    def __init__(self):
        super().__init__()

        self._world = World()
        self._plant_energy = Configs().get_plant_energy()

    def do_action(self, robot, args):
        '''Makes robot eat the plant on the current location.

        @param robot: Instance of `objects.robot.Robot'.
        '''
        if len(args) != 1:
            raise InvalidArgumentsError("`eat' action takes no arguments.")

        try:
            current_square = self._world.get_square(robot.get_location(), for_update=True)
        except LockAlreadyAquiredError:
            # Trying one more time.
            time.sleep(0.02)
            current_square = self._world.get_square(robot.get_location(), for_update=True)

        plant = current_square.get_plant()

        if plant is None:
            raise NoPlantToEat("There's no plant on {0}".format(robot.get_location()))

        if plant.is_matured():
            robot.set_energy(robot.get_energy() + self._plant_energy)

        # Plant will be removed from the world, regardless of its maturity.
        current_square.set_plant(None)
