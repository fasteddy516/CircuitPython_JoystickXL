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

.. literalinclude:: ../examples/boot/standard/boot.py
    
This enables JoystickXL along with CircuitPython's other standard USB HID
devices.  The ``axes``, ``buttons`` and ``hats`` parameters are all set to
maximum values here, but can be lowered if you know you're going to be
using fewer inputs.

Alternatively, if you're not using any other CircuitPython USB-HID devices
and don't want them to appear on the host, you can enable the joystick
device by itself as shown below:

.. literalinclude:: ../examples/boot/minimal/boot.py
    
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

    Adafruit CircuitPython 7.0.0-alpha.5 on 2021-07-21; Adafruit QT Py M0 Haxpress with samd21e18
    >>> from joystick_xl.tools import TestConsole
    >>> TestConsole()

When the test console loads up, you will be greeted with the following:

.. code-block:: text

    JoystickXL - Test Console

    Using 1-based indexing.
    Enter command (? for list)
    :

From here, you can manually activate any axis, button or hat switch and see the
results on the host device.  To see a list of available commands, type ``?`` at
the prompt and press enter.  The avalable commands are:

* ``a`` : **Axis commands**
  
  * ``[i]+`` : Momentarily set axis ``i`` to its maximum value. (ex. ``a1+``)
  * ``[i]-`` : Momentarily set axis ``i`` to its minimum value. (ex. ``a4-``)
  * ``t`` : Test all configured axes by simulating movement on them one at a time. (ex. ``at``)

* ``b`` : **Button commands**

  * ``[i]`` : Click button ``i``.  (ex. ``b12``)
  * ``t`` : Test all configured buttons by simulating clicking them one at a time. (ex. ``bt``)

* ``h`` : **Hat Commands**

  * ``[i]u`` : Click hat switch ``i``'s ``UP`` button. (ex. ``h1u``)
  * ``[i]d`` : Click hat switch ``i``'s ``DOWN`` button. (ex. ``h3d``)
  * ``[i]l`` : Click hat switch ``i``'s ``LEFT`` button. (ex. ``h0l``)
  * ``[i]r`` : Click hat switch ``i``'s ``RIGHT`` button. (ex. ``h2r``)
  * ``t`` : Test all configured hat switches by clicking each position one at a time. (ex. ``ht``)

* ``t`` = Test all configured axes, buttons and hats by cycling through their states one at a time.
* ``0`` = Switch to 0-based indexing
* ``1`` = Switch to 1-based indexing
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
it.  If so, you can use the corresponding test console command (ex. ``a2+``, 
``b7``, ``h3d``, etc.) to trigger the desired input and make sure it registers
in-game.

.. warning::

    Make sure you start the JoystickXL test console before you start the
    application you want to test it with on your host.  If you start the
    application on the host first, it may not detect the joystick.


Testing Tools
=============
The best testing application I have found for Windows is 
`Pointy's Joystick Test Application <http://www.planetpointy.co.uk/joystick-test-application/>`_
which accurately shows the status of the entire set of inputs.  (Note that it relies on
Microsoft's DirectInput, so you may need to install the 
`Microsoft DirectX End-User Runtimes <https://www.microsoft.com/en-ca/download/details.aspx?id=8109>`_
in order to get the application to run.)

There is also a web-based test application at
`gamepad-tester.com <https://gamepad-tester.com/>`_
that works well with up to 6 axes, 32 buttons and 1 hat switch.  

I have done very little testing on Linux platforms, but the little bit I've
done has been using ``jstest`` on a Raspberry Pi command line.