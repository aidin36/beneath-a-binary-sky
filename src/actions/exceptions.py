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


class InvalidArgumentsError(Exception):
    '''Raises if arguments of an action are not correct.'''

class InvalidActionError(Exception):
    '''Raises when specified action does not exists or invalid.'''

class NoWaterError(Exception):
    '''Raises if a robot standing on a dry square tries to pick up water.'''

class RobotHaveNoWaterError(Exception):
    '''Raises if the robot does not carry any water, but tries to water a square.'''
