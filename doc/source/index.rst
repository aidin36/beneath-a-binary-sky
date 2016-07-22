.. highlight:: bash
  :linenothreshold: 5

Beneath a Binary Sky
====================

.. toctree::
  :hidden:

  install
  tutorial
  api


What is it?
-----------

Beneath a Binary Sky is a programming game. It means, players are not humans, but programs. Gamer writes a program (a robot) and set it to live on a simulated world. The goal of each robot is to live longer, and produce more childern.

Unlike most of similar games out there, Beneath a Binary Sky is a peaceful world. The goal is not to kill other robots and prove that you're the strongest, rather it about co-operating to make a better living, a better world.

.. TODO: An image that shows a robot and a plant, and it should note that "robots should cultivate in order to make food".

Beneath a Binary Sky can be used as a tool for researching in Artificial Intelligence (specially Intelligence Agent), or simply as a high level game for programmers.

Outstanding Features
--------------------

* Each robot is controlled by a separate process which communicates with the server through network. Thus, robots can be written in any language, on any platform.

* Robots can clone themselves (producing children).

* All of the rules of the world is configurable.

.. TODO: An image showing the relation between robots and the simulator server.

Free Software
-------------

.. image:: _static/gplv3.png
  :alt: Gnu General Public License, version 3

Beneath a Binary Sky is a free (as in freedom) software. It is published under the terms of Gnu General Public License (GPL) Version 3. The source code is available on `Github <https://github.com/aidin36/beneath-a-binary-sky>`_.

Key Rules of the World
-----------------------

* Each robot can plant as many plants as she wants.

* Plants need water in order to grow. Robots can take water from the specific places on the map (marked as *water*) and pour it on the plants.

* If a plant receive enough water durin its life, it becomes mature. Robots can eat matured plants and gain energy.

* If a plant don't receive water for a while, it will die.

* If a robot ran out of energy, it will die.

* Robots also age. They will die after living for a specific time. They should try to give birth to new children if they want to become extinct.

* Robots need to gain an amout of honour, in order to gain allowance of giving birth. Honour will be given to the robots who contribute to the society, by making plants reach their maturity.

* All of the amounts mentioned above (initial energy, maximum age of robots, required honour to give birth, etc) are configurable.


Download and Install
--------------------

Stable releases can be found on `Github releases page <https://github.com/aidin36/beneath-a-binary-sky/releases>`_.

You can also get the latest source code, either by `downloading a zip file from Github <https://github.com/aidin36/beneath-a-binary-sky/archive/master.zip>`_, or cloning it using *git client*::

    git clone https://github.com/aidin36/beneath-a-binary-sky.git

For instructions about how to install and run it, see :doc:`install`.

