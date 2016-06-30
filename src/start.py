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
import subprocess
import time

from database.memcached_database import MemcachedDatabase
from database.memcached_connection import MemcachedConnection
from objects.robot import Robot


def main():
    # Running new instance of memcached.
    memcached_process = subprocess.Popen(["memcached", "-l", "127.0.0.1", "-p", MemcachedConnection.DEFAULT_PORT])
    # Waiting for the memcache to start.
    time.sleep(0.2)

    # Initializing the database.
    database = MemcachedDatabase()
    database.initialize()

    # Addin a robot, just for testing.
    database.add_robot(Robot("jfhdieu82839", "123"), 2, 1)

    # Actually starting the application.
    os.system("uwsgi --http :9090 --wsgi-file json_listener.py")

    memcached_process.terminate()

if __name__ == "__main__":
    main()
