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

.. literalinclude:: ../examples/simple_test/code.py


Joystick - Basic
================

.. literalinclude:: ../examples/joystick_basic/code.py


Joystick - XL!
==============

(Example coming!)


Multi-Unit HOTAS
================

(Example coming!)