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

import utils.logger
from utils.configs import Configs
from utils.exceptions import BinarySkyException
from database.memcached_database import MemcachedDatabase
from database.exceptions import LockAlreadyAquiredError
from security.authenticator import Authenticator, AuthenticationFailedError
import actions.exceptions as exceptions
from actions.status_action import StatusAction
from actions.sense_action import SenseAction
from actions.move_action import MoveAction
from actions.plant_action import PlantAction
from actions.pick_water import PickWaterAction
from actions.info_action import InfoAction


class ActionManager:

    def __init__(self):
        self._authenticator = Authenticator()
        self._database = MemcachedDatabase()

        configs = Configs()
        self._robots_action_delay = configs.get_robots_actions_delay() / 1000

        self._actions = {'status': StatusAction(),
                         'sense': SenseAction(),
                         'move': MoveAction(),
                         'plant': PlantAction(),
                         'pick_water': PickWaterAction(),
                         'info': InfoAction()}


    def do_action(self, password, action_type, args):
        '''Will do the requested action.'''
        if len(args) == 0:
            raise exceptions.InvalidArgumentsError("`robot_id' should be passes as the first argument.")

        robot_id = args[0]
        if not isinstance(robot_id, str):
            raise exceptions.InvalidArgumentsError(
                "First argument (robot_id) should be a string, not {0}".format(type(robot_id)))

        robot = None
        try:
            robot = self._database.get_robot(robot_id, for_update=True)

            self._authenticator.authenticate_robot(robot, password)

            actions_delay = time.time() - robot.get_last_executed_action_time()
            if actions_delay < self._robots_action_delay:
                # Robot is sending actions too fast. Putting a delay between its actions.
                time.sleep(self._robots_action_delay - actions_delay)

            handler = self._get_action_handler(action_type)

            result = handler.do_action(robot, args)

            # Reducing age and energy.
            robot.set_energy(robot.get_energy() - 1)
            robot.set_life(robot.get_life() - 1)

            # Updating last executed action time.
            robot.set_last_executed_action_time(time.time())

            return result

        except LockAlreadyAquiredError as error:
            # Logging all concurrency errors, so we can investigate them later.
            utils.logger.info("LockAlreadyAquiredError: {0}".format(error))
            raise
        except AuthenticationFailedError:
            raise
        except BinarySkyException:
            # Concurrency exception is a fault of the server. Also, we ignored
            # authentication errors. Otherwise, robot should lose energy and age.

            # Note that we didn't handled unexpected errors (e.g. Exception class).
            # XXX: Dirty code. It shouldn't rollback and/or commit database changes.
            #      But right now, there's no better way.
            self._database.rollback()
            if robot is None:
                # Seems we couldn't even get the robot. So, robot didn't do any actions
                # and shouldn't lose energy and age.
                raise

            robot = self._database.get_robot(robot_id, for_update=True)
            robot.set_energy(robot.get_energy() - 1)
            robot.set_life(robot.get_life() - 1)
            robot.set_last_executed_action_time(time.time())

            self._database.commit()

            raise


    def _get_action_handler(self, action_type):
        '''Returns instance that should handle this action.'''
        if not isinstance(action_type, str):
            raise exceptions.InvalidActionError("Action type must be str, not {0}".format(type(action_type)))

        handler = self._actions.get(action_type)

        if handler is None:
            raise exceptions.InvalidActionError("Action {0} does not exists.".format(action_type))

        return handler
