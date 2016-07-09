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


Commands a Robot Can Send to Server (Actions)
---------------------------------------------

Here is a list of commands a robot can send to the server. These commands calls *Action*.

**info**

Gives general information about the world.

*arguments*: None

*result*: A dictionary with the following keys:

world_size: *string* A string in the form of "x,y".

plant_max_age: *integer* Maximum age a plant can reach. At this age, plant will die.

plant_matured_age: *integer* Age that a plant become matured and eatable by robots.

action_delay: *integer* Minimum delayed time before executing next action. For example, if it is 30, it means a robot
can't do the next action if less than 30 seconds has been passed.

Example result::

    {"status": 200,
     "result": {"world_size": "500,300",
                "plant_max_age": 60,
                "plant_matured_age": 25}
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
=========================================  =====================================

