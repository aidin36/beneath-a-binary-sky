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

from objects.base_object import BaseObject
from objects.exceptions import LongRobotNameError
from utils.configs import Configs

# Note: It's not configurable, because letting too long names can break the database.
MAX_ROBOT_NAME = 32


class Robot(BaseObject):

    def __init__(self, id, password, name=""):
        super(Robot, self).__init__()

        if not isinstance(name, str) or len(name) > MAX_ROBOT_NAME:
            raise LongRobotNameError("Robot name cannot be longer than {0}".format(MAX_ROBOT_NAME))

        configs = Configs()

        self._id = id
        self._name = name
        self._alive = True
        self._password = password
        self._x = 0
        self._y = 0
        self._has_water = False
        self._energy = configs.get_robots_initial_energy()
        self._maximum_energy = configs.get_robots_maximum_energy()
        self._life = configs.get_robots_initial_life()
        self._honor = 0
        self._last_executed_action_time = 0


    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_alive(self):
        return self._alive

    def set_alive(self, alive):
        self._alive = alive

    def get_password(self):
        return self._password

    def get_location(self):
        '''Returns a tuple containing (x, y)'''
        return (self._x, self._y)

    def set_location(self, location):
        self._x = location[0]
        self._y = location[1]

    def set_has_water(self, value):
        self._has_water = value

    def get_has_water(self):
        return self._has_water

    def set_energy(self, value):
        self._energy = min(value, self._maximum_energy)

    def get_energy(self):
        return self._energy

    def set_life(self, value):
        self._life = value

    def get_life(self):
        return self._life

    def set_honor(self, value):
        self._honor = value

    def get_honor(self):
        return self._honor

    def get_last_executed_action_time(self):
        return self._last_executed_action_time

    def set_last_executed_action_time(self, value):
        self._last_executed_action_time = value
