.. highlight:: bash
  :linenothreshold: 5

How to install and run
======================

.. toctree::
  :hidden:

  api

Installing Dependencies
-----------------------

Gnu/Linux
^^^^^^^^^

Beneath a Binary Sky is depend on the followings:

* python3
* libmemcached
* memcached
* nginx
* pylibmc
* uwsgi
* msgpack-python

The following instructions explains how to easily install these dependencies.

First, installing Python 3 and Memcached. On Debian based distros
(like Debian, Ubuntu, Mint, etc), you can simply use ``apt``::

    sudo apt-get install python3 python3-dev python3-pip libmemcached memcached nginx

On other distros, check your package management to find and install these packages.

After that, you can use ``pip3`` to install Python packages. This step is same for all distors::

    sudo pip3 install pylibmc uwsgi msgpack-python


Configuring Nginx
-----------------

The server should be behind a Http Server. Server communicates with the Http Server using UWSGI.

You can find sample configuration files in ``sample_configs/nginx_configs/`` directory. Copy
``binary-sky.conf`` into ``/etc/nginx/sites-enabled/`` directory. Also, copy
``binary-sky.key`` and ``binary-sky.crt`` into ``/etc/nginx/ssl-certs/`` (if directory
doesn't exists, create it).

Using this sample configurations, Nginx and server should work fine. There's some comments
on the config file that explains what these configs mean.

Then, stop and start the Nginx again::

    sudo nginx -s stop
    sudo nginx -s start

**Note**: The certificate files are self-signed certificates, which are not valid. You should
use real signed certificates, if you want to host the server somewhere public.

Security Note
^^^^^^^^^^^^^

By default, Nginx listens on 80 port for any coming HTTP request. This can cause security issues.
If you don't want to use it, it is highly recommended to disable this default site.

To do so, find a ``default`` file or something similar in ``/etc/nginx/sites-enabled/``, and
remove it. It's usually only a link to ``/etc/nginx/sites-available``, and is safe to remove.

Running the server
------------------

Now that Nginx is up and running, you should start the server.

To run the server, switch to ``src`` directory, and run::

    python3 start.py

It will start the server with the default config files. The default configs
should work with the sample config of Nginx, out-of-the-box.

Server configurations
---------------------

This section explains configurations to customize the server behavior.

There is three config files:

Server Configs
^^^^^^^^^^^^^^

This config customizes behavior and rules of the world. Such as, robot's initial energy and
plant's maximum life.

The default config file can be found in ``sample_configs/sample.config``. It contains all the
available options, and explained each of them. Read this to learn about server configurations.

World File
^^^^^^^^^^

The World File defines the map of the world. This file should contains a matrix of numbers.
Each number determines a Square Type, i.e. Soil or Water. All of the matrix's lines should
be in same size. The top left corner of the matrix is 0,0 location.

The default world file is ``sample_configs/small.world``. Use it as a sample to start
creating your own world.

Logging Config
^^^^^^^^^^^^^^

The third config is the Logging Config. This is the Python's logging file. You can find the documentation
of how to config this file on `Python's doc site <https://docs.python.org/3/library/logging.config.html>`_.

For production server, it is recommended to use Syslog for logging. It have lower overhead on server.
To do so, on *handlers* section, change the *keys* option to *syslog*. Then, in *logger_root* section,
change the *handler* option to *syslog*. Note that your Syslog server should be started, or server will
not start.

Providing Different Config Files to Server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, server loads the default config files. If you want to load another file instead,
you can pass options to the *start.py* file. For example::

    python3 start.py --config /path/to/config --world /path/to/world

You can see all the available options by invoking *help*::

    python3 start.py --help


Running Tests
-------------

To check the health of the server (e.g. it will run without any problem on your machine),
you can run tests. To do so, change your directory to *tests*, then simply invoke::

    python3 start.py
