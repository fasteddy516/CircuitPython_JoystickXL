Boot.py
=======

In order to use JoystickXL you have to initialize a custom USB HID device in
the ``boot.py`` file on your CircuitPython device.  If this file does not
currently exist in the root folder on your ``CIRCUITPY`` drive, you can use
the standard example below.

.. note::

    You will have to reset your CircuitPython board after creating or modifying
    ``boot.py`` in order for the changes to be recognized. 

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

This is a fully functional joystick with 2 axes, 2 buttons and a single hat
switch.

.. literalinclude:: ../examples/joystick_basic/code.py


Joystick - Advanced
===================

This is a fully functional joystick with 8 axes, 24 buttons and 4 hat switches.
Notice the only difference between this example and the basic example is the
number of inputs added with ``add_input``. 

.. literalinclude:: ../examples/joystick_advanced/code.py


Multi-Unit HOTAS
================

This is a much more complicated example that uses a pair of Adafruit Grand
Central M4 Express boards to create a HOTAS.  (If you have no idea what that
is, check out the `Thrustmaster Warthog <https://duckduckgo.com/?q=thrustmaster+warthog&t=h_&iax=images&ia=images&kp=1>`_
or `Logitech X56 <https://duckduckgo.com/?q=logitech+x56&t=h_&iax=images&ia=images&kp=1>`_.)

The HOTAS example consists of two physically separate units - the *Throttle*
and the *Stick*.  Each component could have its own USB connection to the host
computer such that the pair appear as two independant USB HID devices, but this
can get complicated because:

1. CircuitPython USB HID game controllers (joystick/gamepad) devices all
   identify themselves to the operating system as ``CircuitPython HID``, which
   makes it difficult to determine which device is which when more than one
   device is connected. 

2. A lot of games/flight sims/racing sims have a difficult time distinguishing
   between multiple controllers, which makes it difficult to get those controls
   configured properly and consistently.

To alleviate these issues, this example uses a wired (UART) connection
between the Throttle and Stick, and a single USB connection from the Stick
to the host computer.  Each piece has 16 buttons, 4 axes and 2 hat switches,
but the whole collection appears to the host computer as a single 32 button,
8 axis, 4 hat switch joystick.

This example makes use of JoystickXL's virtual inputs, which allow raw input
values to be assigned to them in code rather then read directly from GPIO pins.
This functionality can be used in other "remote I/O" situations, such as using
an I2C GPIO expander with a much smaller CircuitPython board.

If you look closely, you'll notice that the only really *complicated* parts
of this example are the bits that deal with the serial communications and the
associated data processing.  Everything else is almost identical to the
*Basic* example above - create a JoystickXL object, associate inputs with it,
make sure you call the jooystick's ``update()`` method in your main loop.

.. literalinclude:: ../examples/hotas/stick/code.py
.. literalinclude:: ../examples/hotas/throttle/code.py
