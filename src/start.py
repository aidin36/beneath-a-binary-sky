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
import argparse
import subprocess
import time

from utils.configs import Configs
from database.memcached_database import MemcachedDatabase
from utils.logger import Logger
from world.world import World


def parse_args():
    print("Beneath a Binary Sky - Copytright (c) 2016 Aidin Gharibnavaz")
    print("")
    print("This is a Free Software, published under the terms of GNU")
    print("General Public License version 3. This program comes with")
    print("ABSOLUTELY NO WARRANTY. For more details, see the COPYING file.")
    print("")

    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--config', dest='config_file',
                        default='../sample_configs/sample.config',
                        help='Config file to load configs from.')
    parser.add_argument('-w', '--world', dest='world_file',
                        default='../sample_configs/small.world',
                        help='World file to load.')
    parser.add_argument('-l', '--logging', dest='logging_config_file',
                        default='../sample_configs/logging.config',
                        help='Logger config file.')

    return parser.parse_args()


def load_configs(config_file):
    configs = Configs()
    configs.load_configs(config_file)

    return configs


def initialize_logger(config_file):
    Logger().load_configs(config_file)


def initialize_database(initial_passwords):
    database = MemcachedDatabase()
    database.initialize()

    for password in initial_passwords:
        database.add_password(password)


def initialize_world(world_file):
    world = World()
    world.load_from_file(world_file)


def start_listeners(workers, args):
    # Passing arguments as an environment argument to the processes.
    env = os.environ
    env.update(BINARY_SKY_CONFIG_FILE=args.config_file,
               BINARY_SKY_LOGGING_FILE=args.logging_config_file)

    json_listener = subprocess.Popen(["uwsgi", "--threads=1", "--processes={0}".format(workers),
                                      "--socket=/tmp/binary-sky.json.socket",
                                      "--module=listeners.json_listener",
                                      "--chmod-socket=666",
                                      "--master"],
                                     env=env)
    msgpack_listener = subprocess.Popen(["uwsgi", "--threads=1", "--processes={0}".format(workers),
                                         "--socket=/tmp/binary-sky.msgpack.socket",
                                         "--module=listeners.msgpack_listener",
                                         "--chmod-socket=666",
                                         "--master"],
                                         env=env)

    # TODO: Find a better way for waiting for the termination.
    msgpack_listener.wait()

def main():
    args = parse_args()

    configs = load_configs(args.config_file)

    # Starting Memcached database.
    memcached_process = subprocess.Popen(["memcached", "-l", "127.0.0.1", "-p", configs.get_server_database_port()])

    # Waiting a little to ensure that Memcached is started.
    time.sleep(0.5)

    try:
        # Sleeping a little, to ensure Memcached is started.
        initialize_logger(args.logging_config_file)

        initialize_database(configs.get_server_initial_passwords())

        initialize_world(args.world_file)

        start_listeners(configs.get_server_workers(), args)

    finally:
        memcached_process.terminate()


if __name__ == "__main__":
    main()
