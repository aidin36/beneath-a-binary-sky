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

from communicator import Communicator


class WaterPickingHandler:
    '''Goes to the last known water location, and picks some.'''

    def handle(self, memory, current_location):

        water_location_x, water_location_y = memory.get_nearest_water().split(',')
        water_location_x = int(water_location_x)
        water_location_y = int(water_location_y)

        current_location_x, current_location_y = current_location.split(',')
        current_location_x = int(current_location_x)
        current_location_y = int(current_location_y)

        print("Current location:", current_location)
        print("Moving to the water location:", water_location_x, ",", water_location_y)

        while current_location_x != water_location_x or current_location_y != water_location_y:
            direction = ""

            # We also update the current location, so we don't need asking server and losing energy.
            if current_location_y < water_location_y:
                direction += "S"
                current_location_y += 1
            if current_location_y > water_location_y:
                direction += "N"
                current_location_y -= 1

            if current_location_x < water_location_x:
                direction += "E"
                current_location_x += 1
            if current_location_x > water_location_x:
                direction += "W"
                current_location_x -= 1

            print("Moving", direction)
            response = Communicator.send_action("move", [direction])
            if response['status'] == 500:
                if response['error_code'] == "LocationIsBlockedError":
                    while True:
                        print("The path is blocked! But I don't know how to by pass a blocked object :/")
                        # Waiting a little, maybe there's a robot or something on the way.
                        time.sleep(0.5)
                        response = Communicator.send_action("move", [direction])
                        if response['status'] == 200:
                            break
                else:
                    print("Unexpected error:", response['error_code'], ":", response['error_message'])


        print("I'm reached the water location. Picking some water.")
        response = Communicator.send_action("pick_water", [])
        if response['status'] == 500:
            print("Unexpected error:", response['error_code'], ":", response['error_message'])
