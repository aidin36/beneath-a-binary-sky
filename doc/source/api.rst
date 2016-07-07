.. highlight:: json
  :linenothreshold: 5

API of the World Server
=======================

This document explains the API that a robot should use to interact with the server.

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
=========================================  =====================================

