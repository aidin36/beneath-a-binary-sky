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
from actions.exceptions import InvalidArgumentsError, RobotHaveNoWaterError
from world.world import World
from database.exceptions import LockAlreadyAquiredError


class WaterAction(Action):

    def __init__(self):
        super().__init__()

        self._world = World()

    def do_action(self, robot, args):
        '''Waters the square robot stands on.

        @param robot: Instance of `objects.robot.Robot'.
        '''
        if len(args) != 1:
            raise InvalidArgumentsError("`water' action takes no arguments.")

        if not robot.get_has_water():
            raise RobotHaveNoWaterError("Robot does not carry water.")

        try:
            square = self._world.get_square(robot.get_location(), for_update=True)
        except LockAlreadyAquiredError:
            # Waiting a little, and trying one more time.
            time.sleep(0.03)
            square = self._world.get_square(robot.get_location(), for_update=True)

        # Note: we don't raise an exception if there's no plant. A robot can waste its water.
        plant = square.get_plant()
        if plant is not None:
            plant.set_water_level(100)

        robot.set_has_water(False)
