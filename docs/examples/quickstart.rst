Installation
============

This library can be easily installed via the Pypi packet manager.

.. code-block:: bash

   pip3 install elmax-api --user


or, to install it globally:

.. code-block:: bash

   pip3 install elmax-api


.. _quickstart:

Quick Start
===========

The following code snippet illustrates how to login to the Elmax Cloud API, fetch the current
zone status and toggle some actuator

   .. literalinclude:: ../../examples/basic.py

Listen for push notifications
=============================

In order to listen for push notification events, it is just necessary to register a callback
coroutine using a `PushNotificationHandler` helper object.

The following example shows how to to so.

   .. literalinclude:: ../../examples/push.py