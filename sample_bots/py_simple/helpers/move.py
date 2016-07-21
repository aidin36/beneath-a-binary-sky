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


def move(from_location, to_location):
    '''Moves the robot from the specified location to the specified location.
    Locations should be strings in form "x,y".
    '''
    to_location_x, to_location_y = to_location.split(',')
    to_location_x = int(to_location_x)
    to_location_y = int(to_location_y)

    from_location_x, from_location_y = from_location.split(',')
    from_location_x = int(from_location_x)
    from_location_y = int(from_location_y)

    print("Current location:", from_location)
    print("Moving to location:", to_location_x, ",", to_location_y)

    while from_location_x != to_location_x or from_location_y != to_location_y:
        direction = ""

        # We also update the current location, so we don't need asking server and losing energy.
        if from_location_y < to_location_y:
            direction += "S"
            from_location_y += 1
        if from_location_y > to_location_y:
            direction += "N"
            from_location_y -= 1

        if from_location_x < to_location_x:
            direction += "E"
            from_location_x += 1
        if from_location_x > to_location_x:
            direction += "W"
            from_location_x -= 1

        print("Moving", direction)
        response = Communicator.send_action("move", [direction])
        if response['status'] == 500:
            if response['error_code'] == "LocationIsBlockedError":
                while True:
                    print("The path is blocked! But I'm not smart enough to pass a blocked object :/")
                    # Waiting a little, maybe there's a robot or something on the way.
                    time.sleep(0.5)
                    response = Communicator.send_action("move", [direction])
                    if not (response['status'] == 500 and response['error_code'] == "LocationIsBlockedError"):
                        # Path cleared, or there's a new error.
                        break
            else:
                print("Unexpected error:", response['error_code'], ":", response['error_message'])
