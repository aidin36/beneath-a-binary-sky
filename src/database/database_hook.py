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


class DatabaseHook:
    '''For hooking database actions, implement this class and registers it.'''

    def robot_got(self, robot_object, locked_for_update):
        '''Calls when a robot got from database. This method can update
        the robot object.

        Should return the `robot_object' again

        @param robot_object: Object got from database.
        @param locked_for_update: If true, it means the object is already locked
            and will be updated on commit.
        '''
        return robot_object

    def square_got(self, location, square_object, locked_for_update):
        '''Calls when a square got from database. This method can update
        the object.

        Should return the `square_object' again

        @param location: location of the square object.
        @param square_object: Object got from database.
        @param locked_for_update: If true, it means the object is already locked
            and will be updated on commit.
        '''
        return square_object
