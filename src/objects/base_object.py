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

class BaseObject:
    '''All the other objects should inherit from this one.'''

    def __init__(self):
        self._dirty = False

    def is_dirty(self):
        '''Returns True if one of the attributes of object changed since its construction.'''
        return self._dirty

    def __setattr__(self, key, value):
        super().__setattr__("_dirty", True)
        super().__setattr__(key, value)
