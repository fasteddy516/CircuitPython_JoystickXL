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
.. note::

    JoystickXL relies on features that were introduced in CircuitPython version 7.0.0.
    **You must be running CircuitPython 7.0.0-alpha3 or newer on your device in order
    to use JoystickXL.**

JoystickXL was made for devices running `Adafruit CircuitPython <https://www.adafruit.com/circuitpython>`_.
For a list of CircuitPython-compatible devices, see `circuitpython.org <https://circuitpython.org/downloads>`_.


Installation
============
(Coming Soon)


Using JoystickXL
================
JoystickXL creates a custom USB-HID device in CircuitPython which requires
some special configuration to enable.  This configuration happens in the
``boot.py`` file in the root folder of the ``CIRCUITPY`` drive.

If this file already exists on your device, you will need to modify it to
include the ``create_joystick()`` function call.  If there is no ``boot.py``
file on your device, you can start with the *standard* example below:


Testing JoystickXL Devices
==========================
* `Pointy's Joystick Test Application <http://www.planetpointy.co.uk/joystick-test-application/>`_
* `Microsoft DirectX End-User Runtimes (June 2010) <https://www.microsoft.com/en-ca/download/details.aspx?id=8109>`_


Documentation
=============
Documentation is available at `<https://circuitpython-joystickxl.readthedocs.org>`_.


Contributing
============
If you have questions, problems, feature requests, etc. please post them to the 
`Issues section on Github <https://github.com/fasteddy516/CircuitPython_JoystickXL/issues>`_.
If you would like to contribute, please let me know.


Acknowledgements
================
(Coming Soon)