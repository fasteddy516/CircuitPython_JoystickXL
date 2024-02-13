Installation
============
1. Download the `latest release of JoystickXL <https://github.com/fasteddy516/CircuitPython_JoystickXL/releases/latest>`_.
2. Extract the files from the downloaded .zip archive.
3. Copy the ``joystick_xl`` folder to the ``lib`` folder on your device's
   ``CIRCUITPY`` drive.

.. seealso::
   
    For additional information on installing libraries, see Adafruit's
    `Welcome to CircuitPython Guide <https://learn.adafruit.com/welcome-to-circuitpython/circuitpython-libraries>`_.


USB HID Configuration
=====================
In order to use JoystickXL you have to initialize a custom USB HID device in
the ``boot.py`` file on your CircuitPython board.  

If ``boot.py`` does not currently exist in the root folder on your board's
``CIRCUITPY`` drive, you can create it using the standard example below:

.. literalinclude:: ../examples/0_boot.py/standard/boot.py
    
This enables JoystickXL along with CircuitPython's other standard USB HID
devices.  The ``axes``, ``buttons`` and ``hats`` parameters are all set to
maximum values here, but can be lowered if you know you're going to be
using fewer inputs.

Alternatively, if you're not using any other CircuitPython USB-HID devices
and don't want them to appear on the host, you can enable the joystick
device by itself as shown below.  (The ``usb_hid.enable()`` function always
expects a tuple - even when it is only given a single device.) 

.. literalinclude:: ../examples/0_boot.py/minimal/boot.py
    
.. note:: 

    Once you're finished creating or modifying ``boot.py`` you will have to
    hard reset your CircuitPython board by pressing its reset button or 
    disconnecting it from power for the changes to take effect.

Once you have ``boot.py`` set up correctly (*and have hard rest your board!*),
you're ready to start working with JoystickXL!  Before you dive into hardware
design and coding, though, you should read over the section on
`Verifying Compatibility`_ below.

.. seealso::

    For more information about customizing USB devices in CircuitPython, you
    can refer to `this excellent guide <https://learn.adafruit.com/customizing-usb-devices-in-circuitpython>`_
    on Adafruit's learning system.


Verifying Compatibility
=======================
Not all platforms/games/applications support joystick devices with high input
counts.  **Before you spend any time writing code or building hardware for a
custom controller, you should make sure the software that you want to use it
with is compatible.**

Fortunately, JoystickXL has a built-in testing module that can be run right
from the CircuitPython Serial Console/REPL to verify compatibility with an
operating system, game or application - *no input wiring or code.py required!*

.. seealso::

    See Adafruit's `Connecting to the Serial Console <https://learn.adafruit.com/welcome-to-circuitpython/kattni-connecting-to-the-serial-console>`_
    and `The REPL <https://learn.adafruit.com/welcome-to-circuitpython/the-repl>`_
    guides for more information about connecting to - and interacting with -
    your board.

Assuming you
have set up ``boot.py`` as described in the `USB HID Configuration`_ section
above, just enter the following two commands at the ``>>>`` prompt in the
CircuitPython REPL to fire up the JoystickXL test console:

.. code-block:: text

    Adafruit CircuitPython 7.0.0-alpha.5 on 2021-07-21; Adafruit Trinket M0 with samd21e18
    >>> from joystick_xl.tools import TestConsole
    >>> TestConsole()

When the test console loads up, you will be greeted with the following:

.. code-block:: text

    JoystickXL - Test Console

    Using 1-based indexing.
    Button Clicks = 0.25s
    Test Button = board.D2
    Enter command (? for list)
    :

From here, you can manually activate any axis, button or hat switch and see the
results on the host device.  To see a list of available commands, type ``?`` at
the prompt and press enter.  The available commands are:

* ``a`` : **Axis commands**
  
  * ``[i]u`` : Move axis ``i`` from idle to its maximum value and back. (ex. ``a1u``)
  * ``[i]d`` : Move axis ``i`` from idle to its minimum value and back. (ex. ``a4d``)
  * ``t`` : Test all configured axes by simulating movement on them one at a time. (ex. ``at``)

* ``b`` : **Button commands**

  * ``[i]`` : Click button ``i``.  (ex. ``b12``)
  * ``t`` : Test all configured buttons by simulating clicking them one at a time. (ex. ``bt``)

* ``h`` : **Hat Commands**

  * ``[i]u`` : Click hat switch ``i``'s ``UP`` button. (ex. ``h1u``)
  * ``[i]d`` : Click hat switch ``i``'s ``DOWN`` button. (ex. ``h3d``)
  * ``[i]l`` : Click hat switch ``i``'s ``LEFT`` button. (ex. ``h0l``)
  * ``[i]r`` : Click hat switch ``i``'s ``RIGHT`` button. (ex. ``h2r``)
  * ``[i]ul`` : Click hat switch ``i``'s ``UP+LEFT`` button. (ex. ``h1ul``)
  * ``[i]ur`` : Click hat switch ``i``'s ``UP+RIGHT`` button. (ex. ``h3ur``)
  * ``[i]dl`` : Click hat switch ``i``'s ``DOWN+LEFT`` button. (ex. ``h0dl``)
  * ``[i]dr`` : Click hat switch ``i``'s ``DOWN+RIGHT`` button. (ex. ``h2dr``)
  * ``t`` : Test all configured hat switches by clicking each position one at a time. (ex. ``ht``)

* ``t`` = Test all configured axes, buttons and hats by cycling through their states one at a time.
* ``0`` = Switch to 0-based indexing
* ``1`` = Switch to 1-based indexing
* ``p[t]`` = Set button press time. (ex. ``p150`` = 1.5 second button presses) 
* ``q`` = Quit the test console

.. note::

    By default, the test console uses **1-based indexing**, which means that
    the first axis is ``1``, first button is ``1``, and so on.  If your host
    device or test application uses **0-based indexing** (the first input is
    ``0``), you can switch the test console to use the same numbering scheme
    with the ``0`` and ``1`` commands.

**If you're using a joystick test application** (one that shows all of the
available inputs and their current states), you can use the ``t`` command
to automatically cycle through all available inputs and make sure they register
in the test app.  You can also test individual input types with their
corresponding test commands, ``at``, ``bt`` and ``ht``.

**To test compatibility with a particular game** you should be able to go to
that game's input configuration settings, select your JoystickXL device
(likely labelled ``CircuitPython HID``) and attempt to assign inputs to
functions.  Ideally, the game uses a *click to assign* system where you
select the desired function, then move/click the input you want to assign to
it.  If so, you can use the corresponding test console command (ex. ``a2u``, 
``b7``, ``h3d``, etc.) to trigger the desired input and make sure it registers
in-game.

.. warning::

    Make sure you start the JoystickXL test console before you start the
    application you want to test it with on your host.  If you start the
    application on the host first, it may not detect the joystick.

**If the application you are trying to test has to be in-focus to capture
joystick events** it will not capture events generated from the test console
because your serial terminal will be in-focus while you are typing in it.
For cases like these, the test console provides a single digital input - by
default on pin ``D2`` (``GP2`` on RP2040-based devices) - which will repeat
the last typed command when activated. You can either hook up an actual
button, or just short the pin to ground to trigger commands as needed.  In
the game example above, you would enter the desired command in the test
console and press enter, then switch to the game and use the button input to
trigger that command while the game is in focus. If needed, the button pin
can also be changed when the test console is started as follows:

.. code-block:: text

    Adafruit CircuitPython 7.0.0-alpha.5 on 2021-07-21; Adafruit Trinket M0 with samd21e18
    >>> import board
    >>> from joystick_xl.tools import TestConsole
    >>> TestConsole(button_pin = board.D7)

.. seealso::
    
    **Joystick Testing Applications**

    * *(Windows)* `Pointy's Joystick Test Application <http://www.planetpointy.co.uk/joystick-test-application/>`_ (requires the `Microsoft DirectX End-User Runtimes <https://www.microsoft.com/en-ca/download/details.aspx?id=8109>`_)
    * *(Browser-based)* `gamepad-tester.com <https://gamepad-tester.com/>`_ (Works with up to 6 axes, 32 buttons and 1 hat switch.)
    * *(Linux)* `jstest <https://linux.die.net/man/1/jstest>`_ (Part of the ``joystick`` package - works with up to 7 axes, 80 buttons, no hat switches)

What Next?
==========

With your configuration in ``boot.py`` complete, and compatibility with your
desired host application confirmed, you're ready to start building and coding!

The *building* part is up to your skills and imagination (and beyond the scope
of this documentation).  Adafruit has some excellent CircuitPython-specific 
guides that can help with the wiring part:

* For Buttons/Hat Switches - `CircuitPython Digital In & Out <https://learn.adafruit.com/circuitpython-essentials/circuitpython-digital-in-out>`_
* For Axes - `CircuitPython Analog In <https://learn.adafruit.com/circuitpython-essentials/circuitpython-analog-in>`_

(Don't worry so much about the code parts in those guides - JoystickXL handles
configuration and processing for standard analog/digital inputs for you -
although it doesn't hurt to know what's going on under the hood!)

Adafruit also carries some excellent
`button <https://www.adafruit.com/?q=button&sort=BestMatch>`_, 
`switch <https://www.adafruit.com/?q=switch&sort=BestMatch>`_,
`rocker <https://www.adafruit.com/?q=rocker&sort=BestMatch>`_,
and `axis <https://www.adafruit.com/?q=joystick&sort=BestMatch>`_
hardware in their store.

The *coding* part is where JoystickXL comes in.  Check out the
:doc:`Examples </examples>` section to see how it's done.  Reading through
the first couple of examples should give you a pretty good sense of
how to get started.  If your custom controller has no more than 24 buttons,
you may be able to use the *More Inputs* example as-is!

If you need to dig deeper into JoystickXL's inner workings, check out the
:doc:`API documentation </api>`.

**Good luck, have fun, and happy coding!**
