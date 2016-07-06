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


class Robot(BaseObject):

    def __init__(self, id, password, name=""):
        super(Robot, self).__init__()

        self._id = id
        self._name = name
        self._alive = True
        self._password = password
        self._x = 0
        self._y = 0

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

    def set_location(self, x, y):
        self._x = x
        self._y = y
