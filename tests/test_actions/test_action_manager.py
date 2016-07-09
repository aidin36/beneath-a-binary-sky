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
import unittest

import actions.exceptions
from actions.action_manager import ActionManager
from database.memcached_database import MemcachedDatabase
from database.exceptions import RobotNotFoundError
from security.authenticator import AuthenticationFailedError
from objects.robot import Robot


class TestActionManager(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestActionManager, self).__init__(*args, **kwargs)

        self._action_manager = ActionManager()
        self._database = MemcachedDatabase()

    def tearDown(self):
        # Rolling back any remaining thing.
        self._database.rollback()

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
        self._database.add_robot(robot, (3, 1))
        self._database.commit()

        with self.assertRaises(AuthenticationFailedError):
            self._action_manager.do_action("ieukjdf-ioquiwe-751io", "status", ["test_invalid_password_95312"])

    def test_dead_robot(self):
        '''Test if ActionManager checks a dead robot.'''
        robot = Robot("test_dead_robot_98176", "1234")
        robot.set_alive(False)
        self._database.add_robot(robot, (3, 2))
        self._database.commit()

        with self.assertRaises(AuthenticationFailedError):
            self._action_manager.do_action("1234", "status", ["test_dead_robot_98176"])

    def test_bad_actions(self):
        '''Test wrong action IDs.'''
        robot = Robot("test_bad_actions_2376", "123")
        self._database.add_robot(robot, (4, 1))
        self._database.commit()

        with self.assertRaises(actions.exceptions.InvalidActionError):
            self._action_manager.do_action("123", "not-exist-action", ["test_bad_actions_2376"])

        self._database.rollback()
        with self.assertRaises(actions.exceptions.InvalidActionError):
            self._action_manager.do_action("123", 5432, ["test_bad_actions_2376"])

        self._database.rollback()
        with self.assertRaises(actions.exceptions.InvalidActionError):
            self._action_manager.do_action("123", None, ["test_bad_actions_2376"])

        self._database.rollback()
        with self.assertRaises(actions.exceptions.InvalidActionError):
            self._action_manager.do_action("123", "", ["test_bad_actions_2376"])

    def test_ok(self):
        '''Execute a fine action.'''
        robot = Robot("test_ok_action_3278", "4467yrt-ddfjh-1u872-oiie")
        self._database.add_robot(robot, (3, 3))
        self._database.commit()

        initial_energy = robot.get_energy()
        initial_age = robot.get_life()

        result = self._action_manager.do_action("4467yrt-ddfjh-1u872-oiie", "status", ["test_ok_action_3278"])

        self.assertEqual(result['alive'], True)

        # Robot should lost energy and age.
        self._database.commit()
        robot = self._database.get_robot("test_ok_action_3278")
        self.assertEqual(robot.get_energy(), initial_energy - 1)
        self.assertEqual(robot.get_life(), initial_age - 1)

    def test_losing_energy_on_error(self):
        '''Tests if ActionManager reduces energy and age after an exception.'''
        robot = Robot("test_losing_energy_on_error_981", "091oikjdmncj")
        self._database.add_robot(robot, (5, 3))
        self._database.commit()

        initial_energy = robot.get_energy()
        initial_age = robot.get_life()

        with self.assertRaises(actions.exceptions.InvalidActionError):
            self._action_manager.do_action("091oikjdmncj", "invalid_action", ["test_losing_energy_on_error_981"])

        self._database.commit()
        robot = self._database.get_robot("test_losing_energy_on_error_981")
        self.assertEqual(robot.get_energy(), initial_energy - 1)
        self.assertEqual(robot.get_life(), initial_age - 1)

        # Robot shouldn't lose energy on authentication error.
        with self.assertRaises(AuthenticationFailedError):
            self._action_manager.do_action("wrong pass", "invalid_action", ["test_losing_energy_on_error_981"])

        self._database.rollback()
        robot = self._database.get_robot("test_losing_energy_on_error_981")
        self.assertEqual(robot.get_energy(), initial_energy - 1)
        self.assertEqual(robot.get_life(), initial_age - 1)

    def test_delay(self):
        '''Tests delay between robot actions.'''
        robot = Robot("test_delay_1223", "09112345")
        self._database.add_robot(robot, (6, 3))
        self._database.commit()

        self._action_manager.do_action("09112345", "sense", [robot.get_id()])
        self._database.commit()

        start_time = time.time()
        self._action_manager.do_action("09112345", "sense", [robot.get_id()])
        elapsed_time = time.time() - start_time
        self._database.commit()

        # one millisecond reduced from delay to cover error.
        self.assertGreater(elapsed_time, 0.029)
