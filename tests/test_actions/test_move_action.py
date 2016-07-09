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

import unittest

from database.memcached_database import MemcachedDatabase
from world.world import World
from world.exceptions import LocationIsBlockedError
from database.exceptions import InvalidLocationError, LockAlreadyAquiredError
from actions.exceptions import InvalidArgumentsError
from actions.action_manager import ActionManager
from objects.robot import Robot


class TestMoveAction(unittest.TestCase):

    def test_directions(self):
        '''Tests if moving in different directions works correctly.'''
        robot_id = "test_directions_154332"
        robot = Robot(robot_id, "123")
        world = World()
        database = MemcachedDatabase()

        world.add_robot(robot, (10, 2))
        database.commit()

        action_manager = ActionManager()

        action_manager.do_action("123", "move", [robot_id, "N"])
        database.commit()
        robot = database.get_robot(robot_id)
        self.assertEqual(robot.get_location(), (10, 1))

        action_manager.do_action("123", "move", [robot_id, "NE"])
        database.commit()
        robot = database.get_robot(robot_id)
        self.assertEqual(robot.get_location(), (11, 0))

        action_manager.do_action("123", "move", [robot_id, "E"])
        database.commit()
        robot = database.get_robot(robot_id)
        self.assertEqual(robot.get_location(), (12, 0))

        action_manager.do_action("123", "move", [robot_id, "SE"])
        database.commit()
        robot = database.get_robot(robot_id)
        self.assertEqual(robot.get_location(), (13, 1))

        action_manager.do_action("123", "move", [robot_id, "S"])
        database.commit()
        robot = database.get_robot(robot_id)
        self.assertEqual(robot.get_location(), (13, 2))

        action_manager.do_action("123", "move", [robot_id, "SW"])
        database.commit()
        robot = database.get_robot(robot_id)
        self.assertEqual(robot.get_location(), (12, 3))

        action_manager.do_action("123", "move", [robot_id, "W"])
        database.commit()
        robot = database.get_robot(robot_id)
        self.assertEqual(robot.get_location(), (11, 3))

        action_manager.do_action("123", "move", [robot_id, "NW"])
        database.commit()
        robot = database.get_robot(robot_id)
        self.assertEqual(robot.get_location(), (10, 2))


    def test_moving_outside(self):
        '''Tests moving a robot to outside of the world.'''
        robot_id = "test_moving_outside_981165"
        robot = Robot(robot_id, "123")
        world = World()
        action_manager = ActionManager()
        database = MemcachedDatabase()

        world.add_robot(robot, (14, 2))
        database.commit()

        with self.assertRaises(InvalidLocationError):
            action_manager.do_action("123", "move", [robot_id, "E"])

        database.rollback()

    def test_blocking_object(self):
        '''Tests moving toward a blocking object.'''
        robot_id = "test_invalid_location_8765112"
        robot = Robot(robot_id, "123")
        world = World()
        action_manager = ActionManager()
        database = MemcachedDatabase()

        world.add_robot(robot, (11, 6))
        database.commit()

        with self.assertRaises(LocationIsBlockedError):
            action_manager.do_action("123", "move", [robot_id, "W"])

    def test_bad_direction(self):
        '''Sends an invalid direction as arguments.'''
        robot_id = "test_bad_direction_18445"
        robot = Robot(robot_id, "123")
        world = World()
        action_manager = ActionManager()
        database = MemcachedDatabase()

        world.add_robot(robot, (12, 6))
        database.commit()

        with self.assertRaises(InvalidArgumentsError):
            action_manager.do_action("123", "move", [robot_id, "U"])

        database.rollback()

        with self.assertRaises(InvalidArgumentsError):
            action_manager.do_action("123", "move", [robot_id, 988])

        database.rollback()

        with self.assertRaises(InvalidArgumentsError):
            action_manager.do_action("123", "move", [robot_id, None])

        database.rollback()

        with self.assertRaises(InvalidArgumentsError):
            action_manager.do_action("123", "move", [robot_id])

        database.rollback()

    def test_lock(self):
        '''Tests if location is locked.'''
        robot_id = "test_move_lock_76120"
        robot = Robot(robot_id, "123")
        world = World()
        action_manager = ActionManager()
        database = MemcachedDatabase()

        world.add_robot(robot, (13, 6))
        database.commit()

        database.get_square((13, 7), for_update=True)

        with self.assertRaises(LockAlreadyAquiredError):
            action_manager.do_action("123", "move", [robot_id, "S"])

        database.rollback()
