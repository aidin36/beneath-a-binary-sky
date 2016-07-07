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

import sys
import time
import os.path
import unittest
import subprocess


def load_configs(current_directory):
    from utils.configs import Configs

    configs = Configs()
    configs.load_configs(os.path.join(current_directory, '..', 'sample_configs', 'tests.config'))

    return configs

def initialize_database():
    from database.memcached_database import MemcachedDatabase

    database = MemcachedDatabase()
    database.initialize()


def initialize_world(current_directory):
    from world.world import World

    world = World()
    world.load_from_file(os.path.join(current_directory, "..", "sample_configs", "tests.world"))


def main():
    # Adding main source directory to the modules path.
    current_module_directory = os.path.abspath(os.path.dirname(sys.modules[__name__].__file__))
    sys.path.insert(0, os.path.join(current_module_directory, '..', 'src'))

    configs = load_configs(current_module_directory)

    # Running new instance of memcached.
    memcached_process = subprocess.Popen(["memcached", "-l", "127.0.0.1", "-p", configs.get_database_port()])

    try:
        # Sleeping a little, to ensure Memcached is started.
        time.sleep(0.5)

        initialize_database()

        initialize_world(current_module_directory)

        # Running tests.
        loader = unittest.TestLoader()
        test_suit = loader.discover(current_module_directory)
        result = unittest.runner.TextTestRunner().run(test_suit)

    finally:
        # Terminating previously started memcached.
        memcached_process.terminate()

    # Setting exit code, so automated scripts would now that tests are failed.
    if not result.wasSuccessful():
        sys.exit(100)

if __name__ == '__main__':
    main()
