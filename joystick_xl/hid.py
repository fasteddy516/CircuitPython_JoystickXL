"""Put a docstring here."""
import usb_hid


def create_joystick() -> usb_hid.Device:
    """Create a usb_hid.Device based on the configured buttons, axes and hats."""
    try:
        from . import config

        _num_buttons = config.buttons
        _num_axes = config.axes
        _num_hats = config.hats
    except ImportError:
        _num_buttons = 64
        _num_axes = 8
        _num_hats = 4

    # Validate the number of configured buttons, axes and hats
    if _num_buttons < 0 or _num_buttons > 64 or _num_buttons % 8 != 0:
        raise ValueError("Button count must be from 0-64 and divisible by 8.")

    if _num_axes < 0 or _num_axes > 8:
        raise ValueError("Axis count must be from 0-8.")

    if _num_hats < 0 or _num_hats > 4 or _num_hats % 2 != 0:
        raise ValueError("Hat count must be from 0-4 and divisible by 2.")

    _report_length = 0

    # fmt: off
    _descriptor = bytearray((
        0x05, 0x01,                         # USAGE_PAGE (Generic Desktop)
        0x09, 0x04,                         # USAGE (Joystick)
        0xA1, 0x01,                         # COLLECTION (Application)
        0x85, 0xFF,                         #   REPORT_ID (Set at runtime, index=7)
    ))

    if _num_buttons > 0:
        _descriptor.extend(bytes((
            0xA1, 0x00,                     #   COLLECTION (Physical)
            0x05, 0x09,                     #     USAGE_PAGE (Button)
            0x19, 0x01,                     #     USAGE_MINIMUM (Button 1)
            0x29, _num_buttons,             #     USAGE_MAXIMUM (num_buttons)
            0x15, 0x00,                     #     LOGICAL_MINIMUM (0)
            0x25, 0x01,                     #     LOGICAL_MAXIMUM (1)
            0x95, _num_buttons,             #     REPORT_COUNT (num_buttons)
            0x75, 0x01,                     #     REPORT_SIZE (1)
            0x81, 0x02,                     #     INPUT (Data,Var,Abs)
            0xC0,                           #   END_COLLECTION
        )))

        _report_length = int(_num_buttons / 8)

    if _num_axes > 0:
        _descriptor.extend(bytes((
            0xA1, 0x00,                     #   COLLECTION (Physical)
            0x05, 0x01,                     #     USAGE_PAGE (Generic Desktop)
        )))

        for i in range(_num_axes):
            _descriptor.extend(bytes((
                0x09, min(0x30 + i, 0x36)   #     USAGE (X,Y,Z,Rx,Ry,Rz,S0,S1)
            )))

        _descriptor.extend(bytes((
            0x15, 0x81,                     #     LOGICAL_MINIMUM (-127)
            0x25, 0x7F,                     #     LOGICAL_MAXIMUM (127)
            0x75, 0x08,                     #     REPORT_SIZE (8)
            0x95, _num_axes,                #     REPORT_COUNT (num_axes)
            0x81, 0x02,                     #     INPUT (Data,Var,Abs)
            0xC0,                           #   END_COLLECTION
        )))

        _report_length += _num_axes

    if _num_hats > 0:
        _descriptor.extend(bytes((
            0xA1, 0x00,                     #   COLLECTION (Physical)
            0x05, 0x01,                     #     USAGE_PAGE (Generic Desktop)
        )))

        for i in range(_num_hats):
            _descriptor.extend(bytes((
                0x09, 0x39,                 #     USAGE (Hat switch)
            )))

        _descriptor.extend(bytes((
            0x65, 0x14,                     #     UNIT (Eng Rot:Angular Pos)
            0x15, 0x00,                     #     LOGICAL_MINIMUM (0)
            0x25, 0x07,                     #     LOGICAL_MAXIMUM (7)
            0x35, 0x00,                     #     PHYSICAL_MINIMUM (0)
            0x46, 0x3B, 0x01,               #     PHYSICAL_MAXIMUM (315)
            0x75, 0x04,                     #     REPORT_SIZE (4)
            0x95, _num_hats,                #     REPORT_COUNT (num_hats)
            0x81, 0x42,                     #     INPUT (Data,Var,Abs,Null)
        )))

        _report_length += int(_num_hats / 2)

    _descriptor.extend(bytes((
        0xC0,                               #   END_COLLECTION
        0xC0,                               # END_COLLECTION
    )))
    # fmt: on

    return usb_hid.Device(
        report_descriptor=bytes(_descriptor),
        usage_page=0x01,  # same as USAGE_PAGE from descriptor above
        usage=0x04,  # same as USAGE from descriptor above
        in_report_length=_report_length,  # length (in bytes) of reports to host
        out_report_length=0,  # length (in bytes) of reports from host
        report_id_index=7,  # 0-based byte position of report id index in descriptor
    )
