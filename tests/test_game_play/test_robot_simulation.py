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
import io
import msgpack

from utils.configs import Configs
from database.memcached_database import MemcachedDatabase
from world.world import World
from objects.map_square import MapSquare
from objects.map_square_types import MapSquareTypes
from objects.robot import Robot
from listeners.msgpack_listener import application


class TestRobotSimulation(unittest.TestCase):

    def setUp(self):
        # Because we create a separate island somewhere out of world, we expand
        # the world's size to cover that island too.
        world = World()
        self._original_world_size = world.get_size()
        world._size = (15, 34)

    def tearDown(self):
        # Setting the world size to its original value.
        world = World()
        world._size = self._original_world_size

    def fake_start_response(self, *args):
        pass

    def post_request(self, request):
        packed_request = io.BytesIO(msgpack.packb(request))

        env = {"REQUEST_METHOD": "POST",
               "wsgi.input": packed_request}

        packed_result = application(env, self.fake_start_response)

        return msgpack.unpackb(packed_result[0], encoding='utf-8')

    def test_robot_simulation(self):
        '''This test simulates a full game scenario.'''
        database = MemcachedDatabase()
        world = World()
        configs = Configs()

        print()
        print("Simulating a robot playing the game. This may take a while.")

        # Creating a world for the robot to live in.
        # The world map is:
        #
        #    000000
        #    000222
        #    000144
        #    000144

        row01 = [MapSquare(MapSquareTypes.SOIL, (0, 30)),
                 MapSquare(MapSquareTypes.SOIL, (1, 30)),
                 MapSquare(MapSquareTypes.SOIL, (2, 30)),
                 MapSquare(MapSquareTypes.SOIL, (3, 30)),
                 MapSquare(MapSquareTypes.SOIL, (4, 30)),
                 MapSquare(MapSquareTypes.SOIL, (5, 30))]
        row02 = [MapSquare(MapSquareTypes.SOIL, (0, 31)),
                 MapSquare(MapSquareTypes.SOIL, (1, 31)),
                 MapSquare(MapSquareTypes.SOIL, (2, 31)),
                 MapSquare(MapSquareTypes.ROCK, (3, 31)),
                 MapSquare(MapSquareTypes.ROCK, (4, 31)),
                 MapSquare(MapSquareTypes.ROCK, (5, 31))]
        row03 = [MapSquare(MapSquareTypes.SOIL, (0, 32)),
                 MapSquare(MapSquareTypes.SOIL, (1, 32)),
                 MapSquare(MapSquareTypes.SOIL, (2, 32)),
                 MapSquare(MapSquareTypes.SAND, (3, 32)),
                 MapSquare(MapSquareTypes.WATER, (4, 32)),
                 MapSquare(MapSquareTypes.WATER, (5, 32))]
        row04 = [MapSquare(MapSquareTypes.SOIL, (0, 33)),
                 MapSquare(MapSquareTypes.SOIL, (1, 33)),
                 MapSquare(MapSquareTypes.SOIL, (2, 33)),
                 MapSquare(MapSquareTypes.SAND, (3, 33)),
                 MapSquare(MapSquareTypes.WATER, (4, 33)),
                 MapSquare(MapSquareTypes.WATER, (5, 33))]

        database.add_square_row(row01)
        database.add_square_row(row02)
        database.add_square_row(row03)
        database.add_square_row(row04)

        # Creating parent of our robot.
        parent_robot = Robot("parent_robot_1982.345", "123", name="Parent")
        parent_robot.set_honor(configs.get_robots_birth_required_honor() + 1)
        world.add_robot(parent_robot, (2, 31))
        database.commit()

        # Giving birth to our hero.
        result = self.post_request({'command': 'give_birth',
                                    'password': '123',
                                    'args': ["parent_robot_1982.345"]})
        self.assertEqual(result['status'], 200, result)
        born_password = result['result']

        # Robot requests a born.
        result = self.post_request({'command': 'born',
                                    'password': born_password,
                                    'args': [parent_robot.get_id()]})
        self.assertEqual(result['status'], 200)
        robot_id = result['result']['robot_id']
        password = result['result']['password']

        # Getting status.
        result = self.post_request({'command': 'status',
                                    'password': password,
                                    'args': [robot_id]})
        self.assertEqual(result['status'], 200, result)
        self.assertTrue(result['result']['alive'])
        self.assertFalse(result['result']['has_water'])
        self.assertEqual(result['result']['location'], "2,30")

        # Moving somewhere to plan a corp.
        # Note that parent robot is on the south. So, we have to turn around it.
        result = self.post_request({'command': 'move',
                                    'password': password,
                                    'args': [robot_id, 'W']})
        self.assertEqual(result['status'], 200, result)
        result = self.post_request({'command': 'move',
                                    'password': password,
                                    'args': [robot_id, 'S']})
        self.assertEqual(result['status'], 200, result)
        result = self.post_request({'command': 'move',
                                    'password': password,
                                    'args': [robot_id, 'S']})
        self.assertEqual(result['status'], 200, result)
        result = self.post_request({'command': 'move',
                                    'password': password,
                                    'args': [robot_id, 'E']})
        self.assertEqual(result['status'], 200, result)

        # We are at the location. Checking if its correct.
        result = self.post_request({'command': 'status',
                                    'password': password,
                                    'args': [robot_id]})
        self.assertEqual(result['status'], 200, result)
        self.assertEqual(result['result']['location'], "2,32")

        # Planting a corp here.
        result = self.post_request({'command': 'plant',
                                    'password': password,
                                    'args': [robot_id]})
        self.assertEqual(result['status'], 200, result)

        # Checking if it is planted.
        result = self.post_request({'command': 'sense',
                                    'password': password,
                                    'args': [robot_id]})
        self.assertEqual(result['status'], 200, result)
        self.assertEqual(result['result']['2,32']['surface_type'], MapSquareTypes.SOIL)
        self.assertIsNotNone(result['result']['2,32']['plant'])

        # Going to pick water.
        result = self.post_request({'command': 'move',
                                    'password': password,
                                    'args': [robot_id, 'E']})
        self.assertEqual(result['status'], 200, result)
        result = self.post_request({'command': 'move',
                                    'password': password,
                                    'args': [robot_id, 'E']})
        self.assertEqual(result['status'], 200, result)

        result = self.post_request({'command': 'pick_water',
                                    'password': password,
                                    'args': [robot_id]})
        self.assertEqual(result['status'], 200, result)

        result = self.post_request({'command': 'status',
                                    'password': password,
                                    'args': [robot_id]})
        self.assertEqual(result['status'], 200, result)
        self.assertTrue(result['result']['has_water'])

        # Getting back to the plant location.
        result = self.post_request({'command': 'move',
                                    'password': password,
                                    'args': [robot_id, 'W']})
        self.assertEqual(result['status'], 200, result)
        result = self.post_request({'command': 'move',
                                    'password': password,
                                    'args': [robot_id, 'W']})
        self.assertEqual(result['status'], 200, result)

        # Watering
        result = self.post_request({'command': 'water',
                                    'password': password,
                                    'args': [robot_id]})
        self.assertEqual(result['status'], 200, result)

        # Checking
        result = self.post_request({'command': 'sense',
                                    'password': password,
                                    'args': [robot_id]})
        self.assertEqual(result['status'], 200, result)
        # It lost some water already.
        self.assertGreater(result['result']['2,32']['plant']['water_level'], 70)

        # Plant should be matured by now. Eating!
        result = self.post_request({'command': 'status',
                                    'password': password,
                                    'args': [robot_id]})
        self.assertEqual(result['status'], 200, result)
        previous_energy = result['result']['energy']

        result = self.post_request({'command': 'eat',
                                    'password': password,
                                    'args': [robot_id]})
        self.assertEqual(result['status'], 200, result)

        result = self.post_request({'command': 'status',
                                    'password': password,
                                    'args': [robot_id]})
        self.assertEqual(result['status'], 200, result)
        self.assertGreater(result['result']['energy'], previous_energy)

        # Now, trying some bad moves!

        # Trying to plant on a sand.
        result = self.post_request({'command': 'move',
                                    'password': password,
                                    'args': [robot_id, 'E']})
        self.assertEqual(result['status'], 200, result)

        result = self.post_request({'command': 'plant',
                                    'password': password,
                                    'args': [robot_id]})
        self.assertEqual(result['status'], 500, result)
        self.assertEqual(result['error_code'], 'CannotPlantHereError')

        # Trying to move to a rock.
        result = self.post_request({'command': 'move',
                                    'password': password,
                                    'args': [robot_id, 'N']})
        self.assertEqual(result['status'], 500, result)
        self.assertEqual(result['error_code'], 'LocationIsBlockedError')
