1. Start Simple
===============

This is a fully functional joystick with 2 axes, 2 buttons and a single hat
switch.

.. literalinclude:: ../examples/1_start_simple/code.py


2. More Inputs!
===============

This is a fully functional joystick with 8 axes, 24 buttons and 4 hat switches.
Notice the only difference between this example and the basic example is the
number of inputs added with ``add_input``. 

.. literalinclude:: ../examples/2_more_inputs/code.py


3. GPIO Expander
================

.. literalinclude:: ../examples/3_gpio_expander/code.py


4. Capacitive Touch
===================

.. literalinclude:: ../examples/4_capacitive_touch/code.py


5. External ADC
===============

.. literalinclude:: ../examples/5_external_adc/code.py


6. Multi-Unit HOTAS
===================

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

2. A number of games/flight sims/racing sims make it difficult to distinguish
   between multiple controllers, which makes it challenging to get those
   controls configured properly and consistently.

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
*Basic* example above - create a JoystickXL object, associate inputs with it
and make sure you call the jooystick's ``update()`` method in your main loop.

.. literalinclude:: ../examples/6_hotas/stick/code.py
.. literalinclude:: ../examples/6_hotas/throttle/code.py
