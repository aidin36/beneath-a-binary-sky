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

from objects.base_object import BaseObject
from utils.configs import Configs


class Plant(BaseObject):

    def __init__(self):
        super().__init__()

        self._age = 0
        self._water_level = 100
        self._last_update = time.time()

    def get_age(self):
        return self._age

    def set_age(self, value):
        self._age = value

    def set_water_level(self, value):
        self._water_level = value

    def get_water_level(self):
        return self._water_level

    def get_last_update(self):
        return self._last_update

    def set_last_update(self, value):
        self._last_update = value

    def is_matured(self):
        return (self._age >= Configs().get_plant_matured_age())
