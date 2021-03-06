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

import time

import helpers.move
from communicator import Communicator


class WaterPickingHandler:
    '''Goes to the last known water location, and picks some.'''

    def handle(self, memory, current_location):
        print("Moving to the latest known water location.")

        helpers.move.move(current_location, memory.get_nearest_water())

        print("I'm reached the water location. Picking some water.")
        response = Communicator.send_action("pick_water", [])
        if response['status'] == 500:
            print("Unexpected error:", response['error_code'], ":", response['error_message'])
