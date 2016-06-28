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


def main():
    # Adding main source directory to the modules path.
    current_module_directory = os.path.abspath(os.path.dirname(sys.modules[__name__].__file__))
    sys.path.insert(0, os.path.join(current_module_directory, '..', 'src'))

    # Running new instance of memcached.
    memcached_process = subprocess.Popen(["memcached", "-l", "127.0.0.1", "-p", "11536"])

    # Sleeping a little, to ensure Memcached is started.
    time.sleep(0.2)

    # Initializing the database with a 10x10 world.
    from database.memcached_database import MemcachedDatabase
    from objects.map_square import MapSquare
    from objects.map_square_types import MapSquareTypes

    database = MemcachedDatabase()
    database.initialize()

    soil_square = MapSquare(MapSquareTypes.SOIL)
    row = []
    for x in range(10):
        row.append(soil_square)

    for y in range(10):
        database.add_square_row(row, y)

    # Running tests.
    loader = unittest.TestLoader()
    test_suit = loader.discover(current_module_directory)
    result = unittest.runner.TextTestRunner().run(test_suit)

    # Terminating previously started memcached.
    memcached_process.terminate()

    # Setting exit code, so automated scripts would now that tests are failed.
    if not result.wasSuccessful():
        sys.exit(100)

if __name__ == '__main__':
    main()
