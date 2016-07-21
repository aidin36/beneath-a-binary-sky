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

from memory import Memory
from communicator import Communicator
from handlers.give_birth_handler import GiveBirthHandler
from handlers.water_finding_handler import WaterFindingHandler
from handlers.water_picking_handler import WaterPickingHandler


class Decider:
    '''This class is responsible for deciding what to do next.
    It only thinks and decide on next action, and then ask
    handlers to do the job.
    '''

    def __init__(self):
        self._memory = Memory()

    def run_til_die(self):
        '''Runs in a loop until the robot dies.'''

        # The algorithm:
        # 1) Find water.
        # 2) Take water and get back to the nearest soil.
        # 3) Plant three corps.
        # 4) Water corps.
        # 5) If honor is enough, give birth to another robot.
        # 6) Continue from 2

        response = Communicator.send_action("info", [])
        if response['status'] == 500:
            print("Unexpected error:", response['error_code'], ":", response['error_message'])
            return

        self._memory.memorize_world_info(response['result'])
        print("I learned these about this world:", response['result'])

        print("Let's explore the world!")
        while True:
            # Checking the status.
            response = Communicator.send_action("status", [])
            if response['status'] == 500:
                # Error occured.
                if response['error_code'] == 'AuthenticationFailedError':
                    print("Seems that I'm dead. Goodbye beautiful world.")
                    break
                else:
                    print("Unexpected error:", response['error_code'], ":", response['error_message'])
                    break

            status = response['result']
            print("My current status is:", status)

            if status['honor'] >= self._memory.get_birth_required_honor():
                print("Enough honor, let's giving birth to a child!")
                GiveBirthHandler().handle(self._memory)

            elif self._memory.get_nearest_water() is None:
                print("I still don't know any water. Let's find some!")
                WaterFindingHandler().handle(self._memory)

            elif not status['has_water']:
                print("No water on hand. Going to pick some.")
                WaterPickingHandler().handle(self._memory, status['location'])
