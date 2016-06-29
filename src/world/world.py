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

from database.memcached_database import MemcachedDatabase
from database.lock import Lock

class World:

    def __init__(self):
        self._database = MemcachedDatabase()

    def get_size(self):
        '''Returns size of the world.'''
        # TODO: World size.
        return (9, 9)

    def add_robot(self, robot, x, y):
        '''Adds a robot to the world.

        @param robot: Instance of objects.robot.Robot.
        @param x: Location of the robot (X)
        @param y: Location of the robot (Y)
        '''
        # TODO: Check for blocking objects.
        with Lock("{0},{1}".format(x, y)):
            self._database.add_robot(robot, x, y)
