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

import traceback

import utils.logger
from database.lock import Lock
from database.memcached_connection import MemcachedConnection
from database.exceptions import CannotAddObjectError, DatabaseFatalError


class Transaction:
    '''Adds a transaction layer to the Memcached.'''

    def __init__(self):
        self._stored_objects = []
        self._new_objects = []
        self._locks = []

    def add_object(self, new_object):
        '''Adds this object to the database on commit.'''
        self._new_objects.append(new_object)

    def store_object(self, object_to_store):
        '''Keeps the object, and updates it on the database if it changes.'''
        self._stored_objects.append(object_to_store)

    def get_lock(self, lock_key):
        '''Gets a lock with the specified key.

        @raise LockAlreadyAquiredError
        '''
        new_lock = Lock(lock_key)
        self._locks.append(new_lock)
        new_lock.aquire()

    def commit(self):
        '''Commits all changes to the database, and releases all the locks.'''
        try:
            self._commit()
        finally:
            self._release_locks()

    def rollback(self):
        '''Clears the stored objects. Note that it won't rollback the changes made
        to the objects themselves. So, if you store an object again, and call commit,
        the changes to that object will be updated on database.

        It releases all the locks.
        '''
        self._stored_objects = []
        self._new_objects = []

        self._release_locks()

    def _commit(self):
        '''Protected commit method.'''
        connection = MemcachedConnection().get_connection()

        # Adding new objects.
        add_list = {x.get_id(): x for x in self._new_objects}
        if len(add_list) > 0:
            errors = connection.add_multi(add_list)

            if len(errors) > 0:
                # Rolling back previously aded objects.
                connection.delete_multi(add_list.keys())

                raise CannotAddObjectError("Could not add these objects to the database: {0}".format(errors))

        # Updating dirty objects.
        update_list = {x.get_id(): x for x in self._stored_objects if x.is_dirty()}

        if len(update_list) > 0:
            set_errors = []
            other_error = None

            try:
                set_errors = connection.set_multi(update_list)
            except Exception as error:
                utils.logger.error("On committing: Error when calling `set_multi': {0}\n{1}".format(
                    error, traceback.format_exc()))
                other_error = error

            if len(set_errors) > 0 or other_error is not None:
                if len(set_errors) > 0 and len(set_errors) != len(update_list):
                    # Some of the objects are updated on the database. We can't rollback them, because
                    # we don't know the previous state of them.
                    raise DatabaseFatalError("An error occurred in setting multi keys, and server couldn't "
                                             "handle this failure. Database may no-longer valid.")

                # Since no object is updated, we can recover by removed all the newly added objects.
                if len(add_list) > 0:
                    delete_result = connection.delete_multi(add_list.keys())

                    if not delete_result:
                        # We couldn't rollback new objects! Very bad!
                        raise DatabaseFatalError(
                            "Server couldn't rollback a failed transaction. Database may no-longer valid.")

            if other_error is not None:
                raise other_error

    def _release_locks(self):
        '''Releases all the previously acquired locks.'''
        for lock in self._locks:
            lock.release()
