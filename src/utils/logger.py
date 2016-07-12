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

import logging
import logging.config

from utils.singleton import Singleton


class Logger(Singleton):

    def _initialize(self):
        pass

    def load_configs(self, config_file_path):
        '''Loads the configurations from the specified path.'''
        logging.config.fileConfig(config_file_path)
        self._logger = logging.getLogger()

    def error(self, log_message):
        '''Logs in ERROR level.'''
        self._logger.error(log_message)

    def info(self, log_message):
        '''Logs in INFO level.'''
        self._logger.info(log_message)
