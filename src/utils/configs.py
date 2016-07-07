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

import configparser

from utils.singleton import Singleton
from utils.exceptions import FatalError


class Configs(Singleton):

    def _initialize(self):
        self._config_parser = configparser.ConfigParser()

    def load_configs(self, config_file_path):
        '''Loads configs from the specified file.'''
        result = self._config_parser.read(config_file_path)

        if len(result) <= 0: # pragma: no coverage
            raise FatalError("Config file {0} not found or is empty.".format(config_file_path))

    def get_database_port(self):
        return self._config_parser.get("database", "port",
                                       fallback=11542)

    def get_robots_initial_energy(self):
        return self._config_parser.get("robots", "initial_energy",
                                       fallback=75)

    def get_robots_maximum_age(self):
        return self._config_parser.get("robots", "maximum_age",
                                       fallback=500)
