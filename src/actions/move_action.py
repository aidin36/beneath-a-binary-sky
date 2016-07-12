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

from utils.logger import Logger
from actions.action import Action
from actions.exceptions import InvalidArgumentsError
from database.exceptions import LockAlreadyAquiredError
from world.world import World


class MoveAction(Action):

    DIRECTIONS = {"N": (0, -1),
                  "NE": (1, -1),
                  "E": (1, 0),
                  "SE": (1, 1),
                  "S": (0, 1),
                  "SW": (-1, 1),
                  "W": (-1, 0),
                  "NW": (-1, -1)}

    def __init__(self):
        self._world = World()
        self._logger = Logger()

    def do_action(self, robot, args):
        '''Move the robot in the specified direction..

        @param robot: Instance of `objects.robot.Robot'.
        '''
        # Validating arguments.
        if len(args) != 2:
            raise InvalidArgumentsError("Move action takes exactly two argument. {0} given.".format(len(args)))

        direction = args[1]
        if not isinstance(direction, str) or direction not in MoveAction.DIRECTIONS:
            raise InvalidArgumentsError("Invalid direction passed to Move action.")

        robot_location = robot.get_location()
        direction_points = MoveAction.DIRECTIONS[direction]
        destination = (robot_location[0] + direction_points[0],
                       robot_location[1] + direction_points[1])

        try:
            self._do_move(robot, destination)
        except LockAlreadyAquiredError:
            # Waiting for a moment, and trying one more time.
            # Client shouldn't receive an error if, for example, someone updating a plant on these squares.
            self._logger.info("Concurrency when trying to move a robot.")
            time.sleep(0.02)
            self._do_move(robot, destination)

    def _do_move(self, robot, destination):
        '''Actually moves the robot to the new location.'''
        self._world.move_robot(robot, destination)
