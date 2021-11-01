Basic Concepts
==============

This library implements an asynchronous HTTP api client against hte Elmax HTTP web endpoint.
The core functionality of the library is implemented within the :class:`elmax_api.http.Elmax` class.

.. warning::

  You need to be familiar with asyncio and python asynchronous programming pattern.
  This library is not designed to work as blocking threaded model.

The HTTP Client
---------------

To get started, simply instantiate an instance of Elmax client:

.. code-block:: python

  # Instantiate the Elmax API client
  client = Elmax(username=MY_USERNAME, password=MY_PASSWORD)


.. note::

  This operation won't attempt any login/connection to the remote cloud, but simply
  construct the client object.

Once created, you can start fetching data from the Elmax Cloud or issuing commands to it.
Have a look at the :ref:`quickstart` section to get your hands dirty right away.


Authentication and login
------------------------

The :py:class:`Elmax` client handles login and authentication autonomously.
Whenever needed, the client will call the login endpoint and authenticates with username/password
provided to the constructor. If the login succeeds, the obtained JWT token is stored into memory for later
use. Thus, everytime the client needs to invoke authenticated APIs, it reuses the cached JTW token.
If, for any reason, the JWT gets refused (as per expiration or invalidation), the library will try again to
renews it using the stored user credentials.

In case the developers wants to check the validity of user-provided credentials, he can explicitly invoke the
:py:func:`login` method, which raises a :py:class:`ElmaxBadLoginError` in case of bad credentials.


Elmax Model
-----------

This library deals with the following entities.

* Panel
   Represents an Elmax Control Panel.
   A Panel is the computational entity which activates actuators and reads zones status.
   A given user, may have multiple panels associated, although this usually means he owns multiple houses/facilities.

* Actuator (switch)
   Is a device that can be activated. It usually has two possible states: on/off.
   The current version of this library handles two main actuator classes: switches (on/off) and covers (up/down).

* Zone (sensor)
   A zone is nothing more than a sensor (volumetric, magnetic, etc).
   Usually a zone represents a specific door/window of the house perimeter.
   As such, a zone can be open or closed.

* Area
   An area is a logical grouping of zones. For instance we can have the kitchen area or the living area.

* Scene
   Scenes are automations that accomplish some objective.
   Common scenes might be "I'm home" (disable alarms open windows) or "I'm leaving" (closes the doors/windows)
   and activates away mode alarm.


Listing Panels
--------------

In order to list the panels associated to the current authenticated user,
simply invoke the :py:func:`list_control_panels` method.
This method returns a list of :py:class:`PanelEntry`, which the developer can use to retrieve the
name/id/online-status of associated control panels.

.. code-block:: python

   # List panels for your user
   panels = await client.list_control_panels()
   print(f"Found {len(panels)} panels for user {client.get_authenticated_username()}")


Fetch panel status
------------------

Given a :py:class:`PanelEntry`, the developer can retrieve its full status by invoking the :py:func:`get_panel_status`
function. This function takes one mandatory argument `control_panel_id` and an optional `pin` code.

.. code-block:: python

   # ...
   # p is a panel entry retrieved via list_control_panels()
   panel_status = await client.get_panel_status(control_panel_id=p.hash)


.. warning::

   The library can only talk to panels that a re currently online. Trying to fetch information from an
   offline panel will likely result an exception being thrown

The panel_status object returned by the client contains information about zones, areas and much more.
Refer to the :py:class:`elmax_api.model.PanelStatus` object for more information.

Send commands to actuators
--------------------------

In order to control actuators connected to the Elmax control panel, the developer must first retrieve the
endpoint_id associated to the device he wants to send the command to. The list of actuators available to a
given panel is available within the :py:attr:`elmax_api.model.PanelStatus.actuators` property.

To send a command to a specicic actuator, the developer relies on :py:func:`execute_command` function.
This function accepts, at minimum, following parameters endpoint_id and command. The former, is the
id of the actuator within the current panel. The latter is the command that the develoepr wants to issue to the device.
The list of accepted commands is described within the :py:mod:`elmax_api.command` module.

The current version of the library supports the following actions:

#. Turn a device on/off

#. Send the UP/DOWN command to a cover

#. Trigger a scene

#. Arm an area

#. Disarm an area
