1. Start Simple
===============

This is a fully functional joystick with 2 axes, 2 buttons and a single hat
switch.

.. literalinclude:: ../examples/1_start_simple/code.py


2. More Inputs!
===============

This is a fully functional joystick with 8 axes, 24 buttons and 4 hat switches.
Notice the only difference between this example and the *Start Simple* example
is the number of inputs added with ``add_input``. 

.. literalinclude:: ../examples/2_more_inputs/code.py


3. Button Operations
====================

This example shows some of the options available for detecting, processing and
bypassing button presses, which can be useful when you want to start adding
things like LEDs and other sensors to your custom controller.

.. literalinclude:: ../examples/3_button_operations/code.py


4. GPIO Expander
================

If you find yourself running out of GPIO pins on your CircuitPython board, you
can add I/O expander peripherals to get the extra pins you need.  The Microchip
MCP23017 is ideal, as Adafruit has a CircuitPython driver for it that lets us
treat the inputs *almost* exactly like on-board pins.

Check out Adafruit's `MCP23017 CircuitPython Guide <https://learn.adafruit.com/using-mcp23008-mcp23017-with-circuitpython>`_
for more information on how to use this peripheral device.

.. literalinclude:: ../examples/4_gpio_expander/code.py


5. External ADC
===============

Similar to the previous example, this one shows how to use an external
analog-to-digital convertor (Microchip MCP3008) to get additional inputs for
axes.

Check out Adafruit's `MCP3008 CircuitPython Guide <https://learn.adafruit.com/mcp3008-spi-adc/python-circuitpython>`_
for more information on how to use this peripheral device.

.. literalinclude:: ../examples/5_external_adc/code.py


6. Capacitive Touch
===================

Adding capacitive touch inputs is simple when you use a device with an existing
CircuitPython driver, such as the Adafruit MPR121 Capacitive Touch Breakout.

Check out Adafruit's `MPR121 Breakout Guide <https://learn.adafruit.com/adafruit-mpr121-12-key-capacitive-touch-sensor-breakout-tutorial/python-circuitpython>`_
for more information on how to use this peripheral device.

.. literalinclude:: ../examples/6_capacitive_touch/code.py


7. Multi-Unit HOTAS
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

If you look closely, you'll notice that the only really *complicated* parts
of this example are the bits that deal with the serial communications and the
associated data processing.  Everything else is almost identical to the
*Start Simple* example above - create a JoystickXL object, associate inputs with it
and make sure you call the jooystick's ``update()`` method in your main loop.

.. literalinclude:: ../examples/7_hotas/stick/code.py
.. literalinclude:: ../examples/7_hotas/throttle/code.py
