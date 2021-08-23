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
to 8 axes, 128 buttons and 4 hat (POV) switches.  If you want to build a custom
game controller with a lot of inputs - *I'm looking at you, space/flight sim
pilots, racing sim drivers and virtual farmers* - JoystickXL can help.

**Head over to the** :doc:`Getting Started </start>` **section to dive in!**


Requirements
============
*This driver relies on features that were introduced in CircuitPython
version 7.0.0.*  **You must be running CircuitPython 7.0.0-alpha3 or newer
on your device in order to use JoystickXL.**

* This driver was made for devices running `Adafruit CircuitPython <https://www.adafruit.com/circuitpython>`_.
  For a list of compatible devices, see `circuitpython.org <https://circuitpython.org/downloads>`_.

* There are no dependencies on any other CircuitPython drivers, libraries or modules.


Host OS/Software Compatibility
==============================
On **Windows 10**, all 8 axes 128 buttons and 4 hat switches are supported at
the operating system level, and JoystickXL has been tested and confirmed to work
with the following games:

* **Microsoft Flight Simulator (2020)** *(All inputs)*
* **Elite Dangerous** *(Limited to 32 buttons)*
* **Star Citizen** *(All inputs)*
* **Digital Combat Simulator (DCS) World** *(All inputs)*
* **Forza Horizon 4** *(All inputs)*
* **BeamNG.drive** *(Limited to 7 axes and 1 hat switch)*
* **Farming Simulator 19** *(Limited to 7 axes, 24 buttons and 1 hat switch)*

*Note that any game-specific input count limitations mentioned above are - to the
best of my knowledge - a result of the game's joystick implementation, and are
not unique to JoystickXL.*

On **Linux**, a very limited amount of testing has been done on a Raspberry Pi
4B using ``jstest`` (part of the ``joystick`` package).  The first 7 axes and
80 buttons work correctly.  Axis 8 does not register any events, nor do any
buttons beyond the first 80.  Only a single hat switch *sort of* works, but it
gets interpreted as two axes rather than an actual hat switch.  Other Linux
platforms/distributions/applications have not been tested.

No testing has been done on an **Apple/Mac** platform.


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
