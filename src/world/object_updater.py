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

import math

from utils.configs import Configs
from database.memcached_database import MemcachedDatabase
from database.database_hook import DatabaseHook
from database.exceptions import LockAlreadyAquiredError


class ObjectUpdater(DatabaseHook):
    '''This class checks objects in the world, and updates them
    if required.

    Responsibilities of this class:
        * Killing and removing a robot from the world, if its
          energy reached zero or it ran out of life.
        * Removing a plant from the world if its water level
          reached zero or it became too old.
        * Maturing a plant if it reached a certain age.
        * Updating a plant's water level during time.
    '''

    def __init__(self):
        self._database = MemcachedDatabase()
        self._configs = Configs()

    def robot_got(self, robot_object, locked_for_update):
        '''Checks and updates the specified robot's object.'''
        if robot_object.get_energy() <= 0 or robot_object.get_life() <= 0:

            if not locked_for_update:
                # This would call this method again, and robot will be updated.
                return self._database.get_robot(robot_object.get_id(), for_update=True)

            robot_object.set_alive(False)

            # Removing the robot from its location.
            try:

                square = self._database.get_square(*robot_object.get_location(), for_update=True)
            except LockAlreadyAquiredError:
                # Trying one more time.
                time.sleep(0.02)
                square = self._database.get_square(*robot_object.get_location(), for_update=True)

            square.set_robot_id(None)

            # XXX: Though it's a very dirty thing to do, we have to commit these changes, because
            #      later this robot will face an Authentication Exception, and our changes will be
            #      lost.
            self._database.commit()

            # Immediately, locking the robot object. It's not atomic, so there's a little chance
            # that concurrency happens. But, it shouldn't be a problem, since the robot is already
            # dead, and can't do anything anyway.
            self._database.get_lock(robot_object.get_id())

        return robot_object

    def square_got(self, location, square_object, locked_for_update):
        '''Checks and updates specified square object.'''
        plant = square_object.get_plant()

        if plant is None:
            return square_object

        # Time passed from the last time this plant updated.
        last_update = time.time() - plant.get_last_update()
        passed_cycles = math.floor(last_update / (self._configs.get_plant_cylce() / 1000))

        if passed_cycles <= 0:
            # No cycle passed, no need to be updated.
            return square_object

        if not locked_for_update:
            # This will call this method again.
            try:
                return self._database.get_square(*location, for_update=True)
            except LockAlreadyAquiredError:
                # Trying one more time.
                time.sleep(0.02)
                return self._database.get_square(*location, for_update=True)

        plant.set_age(plant.get_age() + passed_cycles)
        plant.set_water_level(plant.get_water_level() - (passed_cycles * self._configs.get_plant_lose_water_in_cycle()))

        if plant.get_age() > self._configs.get_plant_max_age() or plant.get_water_level() <= 0:
            # Plant is dead! Removing it from the world.
            square_object.set_plant(None)

        plant.set_last_update(time.time())

        return square_object
