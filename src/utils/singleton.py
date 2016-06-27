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

class Singleton:
    '''If a class derives from this one, it automatically
    become a singleton class.
    
    @note: Don't override __init__ method, override _initialize method
        instead of that.
    '''
    
    _single_instance = None
    _initialized_before = False
    
    def __new__(cls, *args, **kwargs):
        # We check the _single_instance against the type of the class, so
        # every derived class will have its own _single_instance.
        if not isinstance(cls._single_instance, cls):
            cls._single_instance = object.__new__(cls, *args, **kwargs)
        return cls._single_instance

    def __init__(self):
        # It's a singleton class, and it shouldn't initialize more than once.
        if not self._initialized_before:
            self._initialize()
            self._initialized_before = True

    def _initialize(self):
        raise NotImplementedError("You should implement '_initialize' method "
                                  "in your singleton class.")
