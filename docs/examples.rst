Boot.py
=======

JoystickXL creates a custom USB-HID device in CircuitPython which requires
some special configuration to enable.  This configuration happens in the
``boot.py`` file in the root folder of the ``CIRCUITPY`` drive.

.. note::
    USB customization in ``boot.py`` was introduced in CircuitPython version
    7.0.0.  **You must be running CircuitPython 7.0.0-alpha3 or newer on your
    device in order to use JoystickXL.**

If this file already exists on your device, you will need to modify it to
include the ``create_joystick()`` function call.  If there is no ``boot.py``
file on your device, you can start with the *standard* example below:

.. literalinclude:: ../examples/boot/standard/boot.py
    :caption: examples/boot/standard/boot.py

If you're not using any other CircuitPython USB-HID devices, you can enable
the joystick device by itself as shown below:

.. literalinclude:: ../examples/boot/minimal/boot.py
    :caption: examples/boot/minimal/boot.py

For more information about customizing USB devices in CircuitPython, you
can refer to `this excellent guide <https://learn.adafruit.com/customizing-usb-devices-in-circuitpython>`_
on Adafruit's learning system.


Simple Test
===========

This simple test demonstrates the USB HID communications between a
CircuitPython device and a host computer.  It requires no physical input
devices or I/O connections - just use a joystick/gamepad test application
like the ony built-in to Windows to see the various inputs change.

.. literalinclude:: ../examples/simple_test/code.py


Joystick - Basic
================

This is a fully functional joystick with 2 axes, 4 buttons and a single hat
switch.

.. literalinclude:: ../examples/joystick_basic/code.py


Joystick - XL!
==============

This is a more extensible example with 8 axes, 24 buttons and 4 hat switches.
The elements are updated using list comprehensions, so the number of axes,
buttons, and hat switches can be easily adjusted just by adding or removing
elements from their respective lists.  Generation/sending of USB HID reports
is deferred until all inputs are processed to save CPU cycles.

.. literalinclude:: ../examples/joystick_xl/code.py


Multi-Unit HOTAS
================

(Coming soon!)

.. literalinclude:: ../examples/hotas/stick/code.py
.. literalinclude:: ../examples/hotas/throttle/code.py
