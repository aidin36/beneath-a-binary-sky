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

import unittest

import actions.exceptions
from actions.action_manager import ActionManager
from database.memcached_database import MemcachedDatabase
from database.memcached_database import RobotNotFoundError
from database.lock import LockAlreadyAquiredError
from security.authenticator import AuthenticationFailedError
from objects.robot import Robot


class TestActionManager(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestActionManager, self).__init__(*args, **kwargs)

        self._action_manager = ActionManager()
        self._database = MemcachedDatabase()

    def test_not_exist_robot(self):
        '''Test if ActionManager handles not-existed robot.'''
        with self.assertRaises(RobotNotFoundError):
            self._action_manager.do_action("123", "move", ["not_existed_robot_id"])

    def test_bad_robot_id(self):
        '''Test invalid robot IDs.'''
        # Note that listeners checks if `args' is a list, so action manager won't receive another type.

        with self.assertRaises(actions.exceptions.InvalidArgumentsError):
            self._action_manager.do_action("123", "move", [])

        with self.assertRaises(actions.exceptions.InvalidArgumentsError):
            self._action_manager.do_action("123", "move", [None])

    def test_invalid_password(self):
        '''Test if ActionManager authenticate passwords correctly.'''
        robot = Robot("test_invalid_password_95312", "andhue-ifue876-fkdnpw-1")
        self._database.add_robot(robot, 3, 1)

        with self.assertRaises(AuthenticationFailedError):
            self._action_manager.do_action("ieukjdf-ioquiwe-751io", "status", ["test_invalid_password_95312"])

    def test_dead_robot(self):
        '''Test if ActionManager checks a dead robot.'''
        robot = Robot("test_dead_robot_98176", "1234")
        robot.set_alive(False)
        self._database.add_robot(robot, 3, 2)

        with self.assertRaises(AuthenticationFailedError):
            self._action_manager.do_action("1234", "status", ["test_dead_robot_98176"])

    def test_bad_actions(self):
        '''Test wrong action IDs.'''
        # To avoid locking error, a robot is created for each test.

        with self.assertRaises(actions.exceptions.InvalidAction):
            robot = Robot("test_bad_actions_2376_1", "123")
            self._database.add_robot(robot, 4, 1)
            self._action_manager.do_action("123", "not-exist-action", ["test_bad_actions_2376_1"])

        with self.assertRaises(actions.exceptions.InvalidAction):
            robot = Robot("test_bad_actions_2376_2", "123")
            self._database.add_robot(robot, 4, 2)
            self._action_manager.do_action("123", 5432, ["test_bad_actions_2376_2"])

        with self.assertRaises(actions.exceptions.InvalidAction):
            robot = Robot("test_bad_actions_2376_3", "123")
            self._database.add_robot(robot, 4, 3)
            self._action_manager.do_action("123", None, ["test_bad_actions_2376_3"])

        with self.assertRaises(actions.exceptions.InvalidAction):
            robot = Robot("test_bad_actions_2376_4", "123")
            self._database.add_robot(robot, 4, 4)
            self._action_manager.do_action("123", "", ["test_bad_actions_2376_4"])

    def test_ok(self):
        '''Execute a fine action.'''
        robot = Robot("test_ok_action_3278", "4467yrt-ddfjh-1u872-oiie")
        self._database.add_robot(robot, 3, 3)

        self._action_manager.do_action("4467yrt-ddfjh-1u872-oiie", "status", ["test_ok_action_3278"])
