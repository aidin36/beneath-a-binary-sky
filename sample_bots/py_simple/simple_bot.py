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

from communicator import Communicator
from decider import Decider


def main():
    if len(sys.argv) != 2:
        print('Usage: python3 simple_bot.py password')
        sys.exit(101)

    print("A simple robot for Beneath a Binary Sky.")
    print("Author: Aidin Gharibnavaz <aidin@aidinhut.com>")
    print("")

    Communicator.configure("127.0.0.1", 9537)

    print("Borning...")

    Communicator.born(sys.argv[1])

    print("I'm borned!")

    Decider().run_til_die()

if __name__ == '__main__':
    main()
