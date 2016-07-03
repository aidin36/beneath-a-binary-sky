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
import random

ROBOT_ID_PREFIX = "R"
ALL_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-+~!@#$%^&*()_="

class IDGenerator:
    '''Generates unique IDs.'''

    def __init__(self):
        self._pid = os.getpid()
        self._counter = 0

    def get_robot_id(self):
        '''Generates a new unique robot ID.

        @note: It's not thread safe.
        '''
        # Combination of PID and a counter is always unique. But, we add a random number
        # so it can't be easily guess by someone. Yes, it's not very secure, but we
        # don't need that much security anyway!
        result = "{0}.{1}.{2}.{3}".format(ROBOT_ID_PREFIX, self._pid, self._counter, random.randint(0, 999))

        self._counter += 1

        return result

    def get_password(self):
        '''Generates a unique password.'''
        result = ""
        for i in range(16):
            result += random.choice(ALL_CHARS)

        return result
