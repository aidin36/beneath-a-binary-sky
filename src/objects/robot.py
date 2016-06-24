# This file is part of Beneath a Binary Sky.
# Copyright (C) 2016, Aidin Gharibnavaz <aidin@aidinhut.com>
#
# Beneach a Binary Sky is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Beneach a Binary Sky is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Beneach a Binary Sky. If not, see
# <http://www.gnu.org/licenses/>.

class Robot:

    def __init__(self, id, password):
        self._id = id
        self._alive = True
        self._password = password

    def get_id(self):
        return self._id

    def get_alive(self):
        return self._alive

    def set_alive(self, alive):
        self._alive = alive

    def get_password(self):
        return self._password
