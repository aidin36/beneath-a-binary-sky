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

from security.authenticator import Authenticator, AuthenticationFailedError
from objects.robot import Robot


class TestRobotAuthentication(unittest.TestCase):

    def test_ok(self):
        '''A situation that everything is correct.'''
        authenticator = Authenticator()

        robot = Robot("ok_robot_authentication_test", "123")
        authenticator.authenticate_robot(robot, "123")

    def test_wrong_password(self):
        '''Robot sent wrong password.'''
        authenticator = Authenticator()

        robot = Robot("wrong_password_robot_authentication_test", "123")
        with self.assertRaises(AuthenticationFailedError):
            authenticator.authenticate_robot(robot, "187")

    def test_bad_password(self):
        '''When password object is not a string.'''
        authenticator = Authenticator()

        robot = Robot("bad_password_robot_authentication_test", "123")

        with self.assertRaises(AuthenticationFailedError):
            authenticator.authenticate_robot(robot, None)

        with self.assertRaises(AuthenticationFailedError):
            authenticator.authenticate_robot(robot, Robot)

        with self.assertRaises(AuthenticationFailedError):
            authenticator.authenticate_robot(robot, -1)

    def test_dead_robot(self):
        '''Authenticate a dead robot.'''
        authenticator = Authenticator()

        robot = Robot("dead_robot_authentication_test", "123")
        robot.set_alive(False)
        with self.assertRaises(AuthenticationFailedError):
            authenticator.authenticate_robot(robot, "123")
