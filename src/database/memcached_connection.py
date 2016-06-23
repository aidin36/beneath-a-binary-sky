# This file is part of Beneath a Binary Sky.
# Copyright (C) 2016, Aidin Gharibnavaz <aidin@aidinhut.com>
#
# Beneach a Binary Sky is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Beneach a Binary Sky is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Beneach a Binary Sky. If not, see
# <http://www.gnu.org/licenses/>.

import pylibmc

from utils.singleton import Singleton


class MemcachedConnection(Singleton):
    
    def _initialize(self):
        self._mc_client = pylibmc.Client(["127.0.0.1"],
                                         binary=True,
                                         behaviors={"tcp_nodelay": True,
                                                    "ketama": True})

    def get_connection(self):
        return self._mc_client