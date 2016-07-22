.. highlight:: py

Writing a Simple Robot
======================

In this tutorial, we're going to write a simple robot for Benath a Binary Sky.
This robot is not intelligent at all! We're writing this only to get familiar
with the API of the server. You can find some complete examples in *sample_bots*
directory.


Born
----

The first thing a robot should do, is born! By calling *born* command, the physic
of the robot will be created in the server's world.

In order to born, robot needs a password. This is either a pre-defined password, or
a password received from its parent.

Pre-defined passwords are defined in the server
configurations. These will be used when the server is just started, and some new
robots going to join it. Each of these new robots have one of these passwords.
After that, the only way to add new robots to the world is by *giving birth* to
a child robot. When a robot gains enough honor from the society, it can gives birth
to a new robot. (Honor can obtain by watering plants.) Parent robot will be call
*give_birth* command, and in response, receives a new password. It's child can use
this password to *born* in the world.

After born, robot will get a *robot ID* and a new *password*. (The password used for born
is consumed and can't be used again.)

Anyway, let's assume that we a have a password in hand. We're going to send a *born* command
to the server.

In Python, we will do this::

    import sys
    import http.client
    import msgpack

    # First, we create an HTTPS connection to the server. We assumed
    # that server is listen on localhost and 9537 port.
    connection = http.client.HTTPSConnection("127.0.0.1", port=9537)

    # This our request dictionary.
    request = {"command": "born",
               "password": "jhEu23nCod198EnqSx",
               "args": []}

    # Now we pack our request with MsgPack, before sending it to the server.
    packed_request = msgpack.packb(request)

    # Now that our request is ready, we sent it using POST method to ``/msgpack`` URL.
    connection.request("POST", "/msgpack", packed_request)

    # Getting response.
    http_response = connection.getresponse()
    packed_response = http_response.read()

    # Server respond in MsgPack too, so we need to unpack the response
    # before we can use it.
    # We should set the encoding for MsgPack, or else it gives us Bytes
    # instead of Str.
    response = msgpack.unpackb(packed_response, encoding="utf-8")

    # Before continue, we checked if any errors occurred. If there was any error
    # in executing the command, server would set the *status* code of the response to 500.
    if response["status"] == 500:
        print("Error!", response["error_code"], ":", response["error_message"])
        sys.exit(10)

    # there's a "result" key in the response, which contains the ID and Password
    # of the newly borned robot.
    robot_id = response["result"]["robot_id"]
    password = response["result"]["password"]
    print("New Robot ID:", robot_id, "New Password:", password)


Note: We used MsgPack because it's more efficient than JOSN, both in message size and its performance.


Status
------

Now, we're going to send *status* command to the server to obtain status of our robot.

Following our Python example, add these lines to the previous code::

    # New request dictionary. Note that from now on, we should use the
    # ID and the Password that was received from the server before.
    request = {"command": "status",
               "password": password,
               "args": [robot_id]}

    # Packing the request.
    packed_request = msgpack.packb(request)

    # Sending message using POST method.
    connection.request("POST", "/msgpack", packed_request)
    http_response = connection.getresponse()
    packed_response = http_response.read()

    # Unpacking the response as before.
    response = msgpack.unpackb(packed_response, encoding="utf-8")

    # Checking for any error.
    if response["status"] == 500:
        print("Error!", reponse["error_code"], ":", response["error_message"])

    # The result is a dictionary which contains status of our robot.
    result = response["result"]

    print("My current location is", result["location"], ", and I have", result["energy"], "units of energy.")

So simple!

For a complete list of available commands, and error codes, see :doc:`api`.
