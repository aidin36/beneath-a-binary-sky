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

from database.memcached_database import MemcachedDatabase
from database.lock import Lock
from security.authenticator import Authenticator
from actions.exceptions import InvalidArgumentsError


class ActionManager:

    def __init__(self):
        self._authenticator = Authenticator()
        self._database = MemcachedDatabase()


    def do_action(self, password, action_type, args):
        '''Will do the requested action.'''
        if len(args) == 0:
            InvalidArgumentsError("`robot_id' should be passes as the first argument.")

        robot_id = args[0]
        if not isinstance(robot_id, str):
            InvalidArgumentsError("First argument (robot_id) should be a string, not {0}".format(type(robot_id)))

        with Lock(robot_id):
            robot = self._database.get_robot(robot_id)

            self._authenticator.authenticate_robot(robot, password)
