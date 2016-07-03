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

from utils.singleton import Singleton
from database.memcached_database import MemcachedDatabase
from actions.action_manager import ActionManager
from population.population_control import PopulationControl


class Communicator(Singleton):
    '''Interface between listeners and the application.'''

    def _initialize(self):
        self._action_manager = ActionManager()
        self._population_control = PopulationControl()

    def execute_command(self, password, command, args):
        '''Execute client's command.'''

        try:
            if command in ["ui", "stats"]:
                # Admin commands.
                pass
            elif command in ["born", "give_birth"]:
                return self._population_control.execute_command(password, command, args)
            else:
                return self._action_manager.do_action(password, command, args)

        # Committing or rollbacking all changes after the completion of execution.
        except Exception:
            MemcachedDatabase().rollback()
            raise
        else:
            MemcachedDatabase().commit()
