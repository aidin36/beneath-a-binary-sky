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
from helpers.square_types import SquareTypes


class PlantingHandler:
    '''Finds some soil and plants three corps.'''

    def handle(self, memory, current_location):
        print("Moving to the latest known soil.")
        helpers.move.move(current_location, memory.get_nearest_soil())

        print("Checking current location.")
        response = Communicator.send_action("status", [])
        if response['status'] == 500:
            print("Unexpected error:", response['error_code'], ":", response['error_message'])
        status = response['result']

        print("Now I'm at the", status['location'], "location. Planting something.")

        response = Communicator.send_action("plant", [])
        if response['status'] == 500:
            if response['error_code'] == 'AlreadyPlantError':
                print("Strange, but there's already a plant on", status['location'])
                memory.store_first_plant_location(status['location'])
            else:
                print("Unexpected error:", response['error_code'], ":", response['error_message'])
        else:
            memory.store_first_plant_location(status['location'])

        print("Trying to find other soils nearby, and planting on them too.")
        near_soil = self._find_nearby_soil(memory, status['location'])
        if near_soil is None:
            print("Couldn't find any other soils around.")
            return

        helpers.move.move(status['location'], near_soil)

        print("Planting on the founded soil.")
        response = Communicator.send_action("plant", [])
        if response['status'] == 500:
            if response['error_code'] == 'AlreadyPlantError':
                print("Strange, but there's already a plant on", status['location'])
                memory.store_second_plant_location(status['location'])
            else:
                print("Unexpected error:", response['error_code'], ":", response['error_message'])
        else:
            memory.store_second_plant_location(status['location'])


    def _find_nearby_soil(self, memory, current_location):
        '''Check squares around the current location, trying to find a soil.'''
        x, y = current_location.split(',')
        x = int(x) - 1
        y = int(y) - 1

        for j in range(3):
            for i in range(3):
                location_str = "{0},{1}".format(x, y)
                square = memory.get_square(location_str)
                if square is None:
                    # It's somewhere we still didn't discovered, or is out of bounds.
                    continue
                if square['surface_type'] == SquareTypes.SOIL:
                    if location_str != current_location:
                        # Probably current location is soil, but we don't want it.
                        return location_str

                x += 1

            x -= 3
            y += 1

        # Nothing found!
        return None
