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

import helpers.move
from communicator import Communicator


class WateringHandler:
    '''Goes to the location of plants, and waters them.'''

    LAST_WATERED = "second"

    def handle(self, memory, current_location):
        if WateringHandler.LAST_WATERED == "first":
            plant_to_water = memory.get_second_plant_location()
            if plant_to_water is None:
                # There maybe no second plant.
                plant_to_water = memory.get_first_plant_location()
            WateringHandler.LAST_WATERED = "second"
        else:
            plant_to_water = memory.get_first_plant_location()

        print("Going to water", WateringHandler.LAST_WATERED, "plant.")

        helpers.move.move(current_location, plant_to_water)

        print("I reached the plant. Watering...")

        response = Communicator.send_action("water", [])
        if response['status'] == 500:
            print("Unexpected error:", response['error_code'], ":", response['error_message'])
