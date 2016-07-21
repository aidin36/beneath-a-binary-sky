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

import sys
import os
import subprocess

from communicator import Communicator


class GiveBirthHandler:
    '''This handler gives birth to a new child.'''

    def handle(self, memory):
        response = Communicator.send_action("give_birth", [])
        if response['status'] == 500:
            print("Unexpected error:", response['error_code'], ":", response['error_message'])

        new_password = response['result']

        print("Come, come, my little sweetie!")
        current_module_directory = os.path.abspath(os.path.dirname(sys.modules[__name__].__file__))
        main_file = os.path.join(current_module_directory, '..', 'simple_bot.py')

        # Starting the child process. We set its stdout and stderr to ours, so the child can write
        # logs to terminal too.
        child_process = subprocess.Popen(["python3", main_file, new_password], stdout=sys.stdout, stderr=sys.stderr)

        print("My child came to life with PID", child_process.pid)
