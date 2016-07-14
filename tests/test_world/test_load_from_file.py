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

import os
import time
import unittest
import tempfile
import random
import subprocess

from database.memcached_connection import MemcachedConnection
from database.memcached_database import MemcachedDatabase
from world.world import World
from world.exceptions import InvalidWorldFileError
from utils.configs import Configs


class NewWorld:
    '''Creates a fresh server, by creating new instances of World and MemcachedDatabase,
    and starting a new and empty Memcached database.
    '''

    def __enter__(self):
        # Starting a new database on a random port.
        port = random.randrange(11600, 11700)
        self._memcached_process = subprocess.Popen(["memcached", "-l", "127.0.0.1", "-p", str(port)])

        # Waiting for the memcached to start.
        time.sleep(0.5)

        # Forcing the world to create a new instance.
        self._original_world_instance = World._single_instance
        World._single_instance = None

        # Forcing the database to create a new instance.
        self._original_database_instance = MemcachedDatabase._single_instance
        MemcachedDatabase._single_instance = None

        # Initializing the database.
        MemcachedDatabase().initialize()

        # Configuring connection to use this new port.
        mc_connection = MemcachedConnection()
        mc_connection.config_connection(port)


    def __exit__(self, *args):
        # Setting back everything to their original values.
        World._single_instance = self._original_world_instance
        MemcachedDatabase._single_instance = self._original_database_instance
        MemcachedConnection().config_connection(Configs().get_server_database_port())
        self._memcached_process.terminate()


class TestLoadFromFile(unittest.TestCase):

    def test_invalid_length(self):
        '''Tests with a file that one of it's row's length is invalid.'''

        with NewWorld():
            map_data = ("00122\n"
                        "11332\n"
                        "123000\n"
                        "00112\n")

            temp_map_fd, temp_map_file_path = tempfile.mkstemp()
            os.write(temp_map_fd, map_data.encode('utf-8'))
            os.close(temp_map_fd)

            with self.assertRaises(InvalidWorldFileError):
                world = World()
                world.load_from_file(temp_map_file_path)

    def test_not_existed_file(self):
        '''Tries to load a world from a not-existed file.'''
        world = World()
        with self.assertRaises(FileNotFoundError):
            world.load_from_file("a_not_existed_file_12387463")

    def test_invalid_square(self):
        '''Tries to load a file which contains an invalid square number.'''
        with NewWorld():
            map_data = ("00122\n"
                        "11332\n"
                        "12400\n"
                        "00112\n")

            temp_map_fd, temp_map_file_path = tempfile.mkstemp()
            os.write(temp_map_fd, map_data.encode('utf-8'))
            os.close(temp_map_fd)

            with self.assertRaises(InvalidWorldFileError):
                world = World()
                world.load_from_file(temp_map_file_path)
