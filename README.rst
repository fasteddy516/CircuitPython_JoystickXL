JoystickXL for CircuitPython
============================
.. image:: https://img.shields.io/github/license/fasteddy516/CircuitPython_JoystickXL
    :target: https://github.com/fasteddy516/CircuitPython_JoystickXL/blob/master/LICENSE
    :alt: License

.. image:: https://img.shields.io/badge/code%20style-black-000000
    :target: https://github.com/psf/black
    :alt: Black

.. image:: https://readthedocs.org/projects/circuitpython-joystickxl/badge/?version=latest
    :target: https://circuitpython-joystickxl.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://open.vscode.dev/badges/open-in-vscode.svg
    :target: https://open.vscode.dev/fasteddy516/CircuitPython_JoystickXL
    :alt: Open in Visual Studio Code

Description
===========
This CircuitPython driver simulates a *really big* USB HID joystick device - up
to 64 buttons, 8 axes and 4 hat (POV) switches.  If you want to build a custom
game controller with a lot of inputs - *I'm looking at you, space/flight sim
pilots and racing sim drivers* - JoystickXL can help.


Requirements
============
*Note: JoystickXL relies on features that were introduced in CircuitPython
version 7.0.0.*  **You must be running CircuitPython 7.0.0-alpha3 or newer
on your device in order to use JoystickXL.**

* This driver was made for devices running `Adafruit CircuitPython <https://www.adafruit.com/circuitpython>`_.
  For a list of CircuitPython-compatible devices, see `circuitpython.org <https://circuitpython.org/downloads>`_.

* On some of the smaller CircuitPython boards (Trinket M0, Gemma M0, etc.),
  the maximum number of buttons is limited to 24. This is detected and
  enforced automatically.

* There are no dependencies on any other CircuitPython drivers or libraries.


Host OS Compatibility
=====================
* **Windows 10:** All functions work correctly - 64 buttons, 8 axes, 4 hat switches.
* **Linux:** Using ``jstest`` (part of the ``joystick`` package) on a Raspberry Pi,
  all 64 buttons and the first 6 axes work correctly.  The last two axes do not
  work, nor do any of the hat switches.  Other Linux platforms/distributions have
  not been tested.
* **Mac:** Currently untested.


Documentation
=============
Full documentation is available at `<https://circuitpython-joystickxl.readthedocs.org>`_.


Installation
============
1. Download the `latest release of JoystickXL <https://github.com/fasteddy516/CircuitPython_JoystickXL/releases/latest>`_.
2. Extract the files from the downloaded .zip archive.
3. Copy the ``joystick_xl`` folder to the ``lib`` folder on your device's
   ``CIRCUITPY`` drive.

For additional information on installing libraries, see Adafruit's
`Welcome to CircuitPython Guide <https://learn.adafruit.com/welcome-to-circuitpython/circuitpython-libraries>`_.


Using JoystickXL
================
1. Create/modify ``boot.py`` on your CircuitPython device to enable the
   required custom USB HID device.

   .. code:: python

      """boot.py"""
      import usb_hid
      from joystick_xl.hid import create_joystick

      usb_hid.enable((create_joystick()),)

2. Use JoystickXL in ``code.py`` like this:

   .. code:: python
     
      """code.py"""
      import board
      from joystick_xl.inputs import Axis, Button, Hat
      from joystick_xl.joystick import Joystick
   
      js = Joystick()
   
      js.add_input(
          Button(board.D9),
          Button(board.D10),
          Axis(board.A2),
          Axis(board.A3),
          Hat(up=board.D2, down=board.D3, left=board.D4, right=board.D7),
      )

      while True:
          js.update()

   See the `examples <https://circuitpython-joystickxl.readthedocs.io/en/latest/examples.html>`_
   and `API documentation <https://circuitpython-joystickxl.readthedocs.io/en/latest/api.html>`_
   for more information.


Testing JoystickXL Devices
==========================
The best testing application I have found for Windows is 
`Pointy's Joystick Test Application <http://www.planetpointy.co.uk/joystick-test-application/>`_
which accurately shows the status of the entire set of inputs.  Note that you may need to install
the `Microsoft DirectX End-User Runtimes <https://www.microsoft.com/en-ca/download/details.aspx?id=8109>`_
in order to get this application to run.

There is a web-based test application at `<https://gamepad-tester.com/>`_, but
it doesn't get along with JoystickXL.  Axis values don't show up correctly,
and if you have the entire set of inputs enabled, it may not even show up as
a connected device.

I have done very little testing on Linux platforms, but the little bit I've
done has been using ``jstest`` on a Raspberry Pi command line.


Contributing
============
If you have questions, problems, feature requests, etc. please post them to the 
`Issues section on Github <https://github.com/fasteddy516/CircuitPython_JoystickXL/issues>`_.
If you would like to contribute, please let me know.


Acknowledgements
============================
A massive thanks to Adafruit and the entire CircuitPython team for creating and
constantly improving the CircuitPython ecosystem.  

The tools and documentation provided by the `USB Implementors Forum <https://www.usb.org/>`_
were an excellent resource, especially in regards to the creation of the
required USB HID descriptor.  The following resources were particularly useful:

* `HID Descriptor Tool <https://www.usb.org/document-library/hid-descriptor-tool>`_
* `Device Class Definition for HID <https://www.usb.org/document-library/device-class-definition-hid-111>`_
* `HID Usage Tables <https://www.usb.org/document-library/hid-usage-tables-122>`_
