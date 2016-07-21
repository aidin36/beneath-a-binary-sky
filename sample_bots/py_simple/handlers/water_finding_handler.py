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

from communicator import Communicator


class WaterFindingHandler:
    '''This handlers search the world until it finds water.'''

    def __init__(self):
        self._current_direction = "NW"

        # Note that the robot always moves in diagonal directions, to increase
        # the search area.
        self._next_direction = {"NW": "NE",
                                "NE": "SW",
                                "SW": "SE",
                                "SE": "NW"}

    def handle(self, memory):

        while True:
            response = Communicator.send_action("sense", [])
            if response['status'] == 500:
                print("Unexpected error:", response['error_code'], ":", response['error_message'])
                break

            # Updating the memory with these new data.
            result = response['result']
            memory.update_squares(result)

            if memory.get_nearest_water() is not None:
                print("I found water!")
                return

            print("No water yet, moving on ", self._current_direction, "direction.")
            response = Communicator.send_action("move", [self._current_direction])
            if response['status'] == 500:
                if response['error_code'] in ("InvalidLocationError", "LocationIsBlockedError"):
                    self._current_direction = self._next_direction[self._current_direction]
                    print("Changing direction to", self._current_direction)
