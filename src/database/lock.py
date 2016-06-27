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

import pylibmc

from database.memcached_connection import MemcachedConnection


LOCK_POSTFIX = '_L'

class LockAlreadyAquiredError(Exception):
    '''Raises when lock for a specific key is hold by someone else.'''

class Lock:
    '''Handles a lock on database.
    
    Example Usage:
        with Lock(robot_id):
            # Do stuff with database.
    '''

    def __init__(self, key):
        '''@param key: A key in the database you want to lock.'''
        self.__lock_name = "{0}{1}".format(key, LOCK_POSTFIX)

    def aquire(self):
        '''Aquires the lock. Raises exception if lock is already aquired.'''
        mc_connection = MemcachedConnection().get_connection()

        if not mc_connection.add(self.__lock_name, 1):
            raise LockAlreadyAquiredError()

    def release(self):
        '''Releases the lock.
        If the lock wasn't aquired, it will ignore it silently.
        '''
        mc_connection = MemcachedConnection().get_connection()
        mc_connection.delete(self.__lock_name)

    def __enter__(self):
        self.aquire()

    def __exit__(self, *args):
        self.release()
