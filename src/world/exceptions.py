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

from utils.exceptions import BinarySkyException


class InvalidWorldFileError(BinarySkyException):
    '''Raises if there's something wrong with the specified world file.'''

class WorldIsFullError(BinarySkyException):
    '''Raises if no free square is available in the world!'''

class LocationIsBlockedError(BinarySkyException):
    '''Raises if a location is blocked, i.e. a robot tried to move to a blocked location.'''

class AlreadyPlantError(BinarySkyException):
    '''Raises if a robot tries to plant on a location that already contains a plant.'''

class CannotPlantHereError(BinarySkyException):
    '''Raises if a robot tries to plant on a non-soil square.'''
