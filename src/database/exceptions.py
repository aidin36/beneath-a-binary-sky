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


class DatabaseException(Exception):
    '''Base of errors in the database module.'''

class CannotAddRobotError(DatabaseException):
    '''Raises when there is a problem for adding a robot to the database.
    Common causes:
        Robot ID is already exists.
        Memcached is not started.
        Memory is full.
    '''

class RobotNotFoundError(DatabaseException):
    '''Raises if a robot cannot be found on the database.'''

class CouldNotSetValueBecauseOfConcurrencyError(DatabaseException):
    '''Raises if concurrent requests doesn't allow the database to set a value.'''

class InvalidPasswordError(DatabaseException):
    '''Raises if poping a password requested, but it does not exists.'''

class DuplicatedPasswordError(DatabaseException):
    '''Raises if a password is already exists on the database.'''

class InvalidLocationError(DatabaseException):
    '''Raises if the specified location is invalid.'''
