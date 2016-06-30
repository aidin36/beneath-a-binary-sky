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

from security.authenticator import Authenticator
from database.memcached_database import MemcachedDatabase
from world.world import World
from objects.robot import Robot
from utils.id_generator import IDGenerator


class PopulationControl:
    '''Controls the population of the world. i.e. controlling if a robot
    can have a child, or gives birth to new robots.
    '''

    def __init__(self):
        self._authenticator = Authenticator()
        self._database = MemcachedDatabase()
        self._world = World()
        self._robot_id_generator = IDGenerator()

    def execute_command(self, password, command, args):
        '''Executes the specified command.'''
        if command == "born":
            return self._born(password, args)
        elif command == "give_birth":
            self._give_birth(password, args)

    def _born(self, password, args):
        '''Gives birth to a robot for the first time.

        @param args: List of arguments.
            The first argument can be a parent robot. If provided, the
            new robot will be born software near its parent. If not, it
            will be born on a random place.
        '''
        if len(args) > 0:
            parent_robot_id = args[0]

            parent_robot = self._database.get_robot(parent_robot_id)
            born_location = parent_robot.get_location()
        else:
            world_size = self._world.get_size()
            born_location = (random.randint(0, world_size[0] - 1),
                             random.randint(0, world_size[1] - 1))

        self._authenticator.authenticate_new_robot(password)

        new_robot = Robot(self._robot_id_generator.get_robot_id(),
                          self._robot_id_generator.get_password())

        self._world.add_robot(new_robot, born_location[0], born_location[1])

        return {'robot_id': new_robot.get_id(),
                'password': new_robot.get_password()}

    def _give_birth(self, password, args):
        pass
