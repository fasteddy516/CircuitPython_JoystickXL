``joytsick_xl.hid``
===============================
.. automodule:: joystick_xl.hid
   :members:

``joystick_xl.joystick``
=========================================
.. automodule:: joystick_xl.joystick
   :members:

``joystick_xl.helpers``
=======================================
.. automodule:: joystick_xl.helpers
   :members:

``config.py``
=============
By default, JoystickXL creates a USB HID joystick device with 64 buttons, 8 axes
and 4 hat switches.  You can lower the number of reported inputs by placing a
``config.py`` file in the JoystickXL library folder (usually ``lib/joystick_xl``
on the ``CIRCUITPY`` drive).  Below is a sample file configured for 8 buttons, 
2 axes and no hat switches:
   
.. code-block:: python
   
   """Sample JoystickXL config.py file."""
   
   buttons = 8  # button count (0-64) in increments of 8
   axes = 2     # axis count (0-8)
   hats = 0     # hat switch count (0-4) in increments of 2

.. note::
   All three variables (``buttons``, ``axes``, ``hats``) **must** be defined in
   ``config.py``, otherwise the file will be ignored and default values will be used.