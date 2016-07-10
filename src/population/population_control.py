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

import random

from actions.exceptions import InvalidArgumentsError
from database.exceptions import DuplicatedPasswordError
from population.exceptions import NotEnoughHonorError
from security.authenticator import Authenticator
from database.memcached_database import MemcachedDatabase
from world.world import World
from objects.robot import Robot
from utils.id_generator import IDGenerator
from utils.configs import Configs


class PopulationControl:
    '''Controls the population of the world. i.e. controlling if a robot
    can have a child, or gives birth to new robots.
    '''

    def __init__(self):
        self._authenticator = Authenticator()
        self._database = MemcachedDatabase()
        self._world = World()
        self._id_generator = IDGenerator()
        self._configs = Configs()

    def execute_command(self, password, command, args):
        '''Executes the specified command.'''
        if not isinstance(password, str):
            raise InvalidArgumentsError("Expected {0} as password, found {1}.".format(type(str), type(password)))

        if command == "born":
            return self._born(password, args)
        elif command == "give_birth":
            return self._give_birth(password, args)

    def _born(self, password, args):
        '''Gives birth to a robot for the first time.

        @param args: List of arguments.
            The first argument can be a parent robot. If provided, the
            new robot will be born software near its parent. If not, it
            will be born on a random place.
        '''
        parent_robot_id = None
        if len(args) > 0:
            parent_robot_id = args[0]

        if parent_robot_id is not None:
            if not isinstance(parent_robot_id, str):
                raise InvalidArgumentsError("`parent_robot_id' must be `str', not {0}".format(type(parent_robot_id)))

            parent_robot = self._database.get_robot(parent_robot_id)
            born_location = parent_robot.get_location()
        else:
            world_size = self._world.get_size()
            born_location = (random.randint(0, world_size[0] - 1),
                             random.randint(0, world_size[1] - 1))

        robot_name = ""
        if len(args) == 2:
            robot_name = args[1]

        self._authenticator.authenticate_new_robot(password)

        new_robot = Robot(self._id_generator.get_robot_id(),
                          self._id_generator.get_password(),
                          name=robot_name)

        self._world.add_robot(new_robot, (born_location[0], born_location[1]))

        return {'robot_id': new_robot.get_id(),
                'password': new_robot.get_password()}

    def _give_birth(self, password, args):
        '''Checks if robot has the permission to give birth to a child.
        If so, it generates and returns a new password.
        '''
        if len(args) != 1:
            raise InvalidArgumentsError("`give_birth' takes exactly one argument.")

        robot_id = args[0]
        if not isinstance(robot_id, str):
            raise InvalidArgumentsError("Expected {0} as robot_id, found {1}".format(type(str), type(args[0])))

        robot = self._database.get_robot(robot_id, for_update=True)

        required_honor = self._configs.get_robots_birth_required_honor()
        if robot.get_honor() < required_honor:
            raise NotEnoughHonorError("Robot needs {0} honor to give birth, but has {1}.".format(
                required_honor, robot.get_honor()))

        robot.set_honor(robot.get_honor() - required_honor)

        # This while is exists, to prevent generating duplicated passwords.
        while True:
            try:
                new_password = self._id_generator.get_password()
                self._database.add_password(new_password)
                break
            except DuplicatedPasswordError: # pragma: no cover
                continue

        return new_password
