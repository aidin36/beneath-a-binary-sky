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


class EatingHandler:
    '''Eats the plant on the current location, if it's matured.'''

    def handle(self, memory, current_location):
        print("Checking if we can eat this plant.")
        response = Communicator.send_action('sense', [])
        if response['status'] == 500:
            print("Unexpected error:", response['error_code'], ":", response['error_message'])
            return

        result = response['result']
        memory.update_squares(result)

        square = memory.get_square(current_location)

        if square['plant'] is None:
            print("No plant! No plant! Where is my delicious plant!")
            print("I have to plant another one :/")
            self._plant()
            return

        if not square['plant']['matured']:
            print("This plant is not matured, have to wait more.")
            return

        print("Eating this yummy plant!")
        response = Communicator.send_action('eat', [])
        if response['status'] == 500:
            print("Unexpected error:", response['error_code'], ":", response['error_message'])

        print("Planting another one here.")
        self._plant()

    def _plant(self):
        response = Communicator.send_action('plant', [])
        if response['status'] == 500:
            print("Unexpected error:", response['error_code'], ":", response['error_message'])
