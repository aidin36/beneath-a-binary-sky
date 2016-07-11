.. highlight:: json

API of the World Server
=======================

This document explains the API that a robot should use to interact with the server.

Surface Types
-------------

Each square on the map, is of a type. Each of these types have their own properties.

The following enumeration defines these types:

0: Soil, 1: Sand, 2: Rock, 3: Water

Plants can only be plant on Soil.

Plant cannot be plant on Sand.

Rock will block the way. Robots cannot pass rocks.

Water is where robots can pick waters. Robots can walk on water.

Commands Related to Birth
-------------------------

**born**

This is the first command a robot should send to the server. By executing this command, robot will
be added to the world. You can think of it as login.

*arguments*: The password argument of this command, is one of the pre-definied passwords on
the server. This is a one-time password.

An optional Parent ID can also be send to the server. If Parent ID passed, the new robot will be
born somewhere close to its parent.

*result*: A dictionary, containing ID and password of the new robot. This password is the one
that should be send along with every command.

Example of command::

    {"password": "oi98Ey12Ncy7Er90",
     "command": "born",
     "args": []}

Example of command with a Parent ID::

    {"password": "Mn81Ey19Ncy7Z2xD",
     "command": "born",
     "args": ["8112.10.910"]}


Example of Result::


    {"status": 200,
     "result": {"robot_id": "8932.23.908",
                "password": "uyhDQpe91U3D3q91"}
     }


**give_birth**

When robot gain enough honor (by watering plants), it can give birth to a new robot. For doing so,
it should send *give_birth* command to the server, and receive a one-time password. Then, child
should send a *born* command with this password to the server.

*arguments*: Like actions, only the password and robot ID is required.

*result*: The one-time password.

Example command::

    {"password": "i87Nco1E32dEwq10",
     "command": "give_birth",
     "args": ["1223.80.127"]
    }

Example result::

    {"status": 200,
     "result": {"nuEy129EcpI29QxP"}
    }


Commands to Control the Robot (Actions)
---------------------------------------

Here is a list of commands a robot can send to the server. These commands calls *Action*.

The arguments listed in from of *arguments*, is the ones inside the *args* list in the command.
The *password* and *robot_id* should always present, so omited from the document.

**info**

Gives general information about the world.

*arguments*: None

*result*: A dictionary with the following keys:

world_size: *string* A string in the form of "x,y".

plant_max_age: *integer* Maximum age a plant can reach. At this age, plant will die.

plant_matured_age: *integer* Age that a plant become matured and eatable by robots.

action_delay: *integer* Minimum delayed time before executing next action. For example, if it is 30, it means a robot
can't do the next action if less than 30 milliseconds has been passed.

maximum_energy: *integer* The maximum energy a robot can have. Eating plants can increase the robot's energy
only to this maximum amount.

birth_required_honor: *integer* The amount of honor required for giving birth to a new child.

Example result::

    {"status": 200,
     "result": {"world_size": "500,300",
                "plant_max_age": 60,
                "plant_matured_age": 25,
                "action_delay": 30,
                "maximum_energy": 400,
                "birth_required_honor": 40}
     }

**move**

Moves the robot in the specified direction.

*arguments*: A string indicating the direction. Direction can be one of *N, NE, NW, E, W, S, SW, SE*.

*result*: None

Example command::

   {"password": "jnh8712ErPn18Ws0",
    "command": "move",
    "args": ["1187.6.167",
             "NE"]
    }

**pick_water**

Makes robot picking up water. Robot should be on a *water* square, or else an excepion will be raised.

*arguments*: None

*result*: None

**plant**

Plants a plant on the location of the robot. If the square is not Soil, an exception will be raised.

*arguments*: None

*result*: None

**sense**

Returns what sensors of the robot can sense. It will returns information about the eight squares around the robot,
and the square robot is standing on.

*arguments*: None

*result*: A dictionary which maps each location to its objects.

Each element of the result dictionary, have these keys:

surface_type: *integer* Type of that surface.

robot: *boolean* If True, it means there's a robot on that square. Note that *sense* command returns the current
location of the robot, too. Since robot is standing there, the *robot* flag of that square is always True.

plant: A dictionary contains infomration about a plant in that location. This can be ``null``, showing no plant is
there.

The *plant* dictionary contains the following keys:

water_level: *integer* Water level of that plant. It can be between zero and 100.

matured: *boolean* If True, shows that plant is matured and can be eat by robots.

age: *integer* Age of the plant. After a certain age, plants will die.

Example result::

    {"status": 200,
     "result": {"2,3": {"surface_type": 0,
                        "robot": true,
                        "plant": {"water_level": 75,
                                  "matured": false,
                                  "age": 7}
                        },
                "2,4": {"surface_type": 1,
                        "robot": false,
                        "plant": null
                        }
                }
    }


**status**

Returns information about the current status of the robot.

*arguments*: None

*result*: A dictionary containing the following fields:

alive: *boolean* If True, it means robot is alive. False mean robot is dead.

location: *string* A string in the form of "x,y", showing where the robot is.

have_water: *boolean* If True, it means robot is carring water.

Example result::

    {"status": 200,
     "result": {"alive": true,
                "location": "26,3",
                "have_water": false}
    }


**water**

Makes the robot pour the water its carrying. It use to water plants. The water level of the plant will become 100
after watering.

Note that if there's no plant on the current location, no exception would be raise. In other words, robot should
be intelligent enough to not waste its water.

*arguments*: None

*result*: None


**eat**

Orders the robot to eat the plant in the current location. If the plant is matured, the robot will receive energy.
Else, plant will be removed from the world, but robot will gain nothing.

Client receives an error if there's no plant on the robot's location.

*arguments*: None

*result*: None


Exceptions
----------

If any errors occur, client will receive a dictionary like these::

    {"status": 500,
     "error_code": "AuthenticationFailedError",
     "error_message": "Wrong password for Robot 6542.6.876"}

=========================================  =====================================
Error Code                                 Description
=========================================  =====================================
InvalidJSONError                           The JSON client sent is in a wrong format, or missed some mandatory fields.
InvalidHttpMethodError                     Server only accepts POST HTTP method. Client will receive this error if it tries to use other method.
InvalidArgumentsError                      Raises if arguments of an action (command) are not correct.
InvalidActionError                         Raises when specified command (action) does not exists or invalid.
DatabaseException                          Normally, client shouldn't receive this error. Most of the times, it means there's something wrong with the server.
CannotAddObjectError                       Raises when there is a problem for adding an object (i.e a robot) to the database.
                                           Common causes:

                                           Object (Robot) ID is already exists.

                                           Memcached is not started.

                                           Memory is full.
RobotNotFoundError                         Raises if a robot cannot be found on the database. Usually, because the provided robot ID is wrong.
CouldNotSetValueBecauseOfConcurrencyError  Raises if two or more concurrent requests received by server and it couldn't handle it. Upon receiving this, client should retry its previous request.
InvalidPasswordError                       Specified password is wrong.
InvalidLocationError                       Specified location is not valid. For example, it's out of the world.
LockAlreadyAquiredError                    Two or more concurrent requests happened and server couldn't handle it. Client should retry its action.
AuthenticationFailedError                  Raises if a robot could not be authenticated. i.e. it's password is wrong, or it's dead.
WorldIsFullError                           Normally, it shouldn't happen! If it is, it means all the world is filled with blocking objects. No one can move!
LocationIsBlockedError                     Raises if a location is blocked, i.e. a robot tried to move to a location that blocked with a rock.
AlreadyPlantError                          Raises if a robot tries to plant on a location that already contains a plant.
CannotPlantHereError                       Raises if a robot tries to plant on a non-soil square.
LongRobotNameError                         Raises if name of a robot is too long.
NoWaterError                               Raises if a robot tries to pick up water from a dry square.
RobotHaveNoWaterError                      Raises if the robot does not carry any water, but tries to water a square.
NotEnoughHonorError                        Raises if a robot doesn't have enough honor to give birth to a child.
=========================================  =====================================

