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
from security.authenticator import Authenticator
import actions.exceptions as exceptions
from actions.status_action import StatusAction
from actions.sense_action import SenseAction
from actions.move_action import MoveAction
from actions.plant_action import PlantAction
from actions.pick_water import PickWaterAction


class ActionManager:

    def __init__(self):
        self._authenticator = Authenticator()
        self._database = MemcachedDatabase()

        self._actions = {'status': StatusAction(),
                         'sense': SenseAction(),
                         'move': MoveAction(),
                         'plant': PlantAction(),
                         'pick_water': PickWaterAction()}


    def do_action(self, password, action_type, args):
        '''Will do the requested action.'''
        if len(args) == 0:
            raise exceptions.InvalidArgumentsError("`robot_id' should be passes as the first argument.")

        robot_id = args[0]
        if not isinstance(robot_id, str):
            raise exceptions.InvalidArgumentsError(
                "First argument (robot_id) should be a string, not {0}".format(type(robot_id)))

        robot = self._database.get_robot(robot_id, for_update=True)

        self._authenticator.authenticate_robot(robot, password)

        handler = self._get_action_handler(action_type)

        return handler.do_action(robot, args)

    def _get_action_handler(self, action_type):
        '''Returns instance that should handle this action.'''
        if not isinstance(action_type, str):
            raise exceptions.InvalidActionError("Action type must be str, not {0}".format(type(action_type)))

        handler = self._actions.get(action_type)

        if handler is None:
            raise exceptions.InvalidActionError("Action {0} does not exists.".format(action_type))

        return handler
