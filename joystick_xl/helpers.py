"""Classes to help process joystick inputs."""

try:
    from typing import Union
except ImportError:
    pass

from digitalio import DigitalInOut, Direction, Pull  # type: ignore
from microcontroller import Pin  # type: ignore


class VirtualInput:
    """Provide an object with a .value property to represent an input."""

    def __init__(self, value: Union[bool, int]) -> None:
        """Set initial .value property (True for buttons, 32768 for axes)."""
        self.value = value


class Axis:
    """Data source storage and scaling/deadband processing for an axis input."""

    @property
    def min(self) -> int:
        """Return the configured minimum raw ``analogio`` input value."""
        return self._min

    @property
    def max(self) -> int:
        """Return the configured maximum raw ``analogio`` input value."""
        return self._max

    @property
    def deadband(self) -> int:
        """Return the raw, absolute value of the configured deadband."""
        return self._deadband

    @property
    def invert(self) -> bool:
        """Return ``True`` if the raw `analogio` input value is inverted."""
        return self._invert < 0

    @property
    def value(self) -> int:
        """Return the current, fully processed value of this axis."""
        return self._value

    def __init__(
        self,
        source,
        deadband: int = 0,
        min: int = 0,
        max: int = 65535,
        invert: bool = False,
    ) -> None:
        """Create an axis object using the specified input data source object."""
        if not hasattr(source, "value"):
            raise ValueError("Axis source must be an object with a 'value' attribute.")
        self._source = source
        self._deadband = deadband
        self._min = min
        self._max = max
        if invert:
            self._invert = -1
        else:
            self._invert = 1
        self._value = 0

        # calculate raw input midpoint and scaled deadband range
        self._raw_midpoint = self._min + ((self._max - self._min) // 2)
        self._db_range = self._max - self._min - (self._deadband * 2)

    def set_source_value(self, value: int) -> int:
        """Set the value property for VirtualInput sources."""
        if isinstance(self._source, VirtualInput):
            self._source.value = value
            return value
        else:
            raise TypeError("Only VirtualInput source values can be set manually.")

    def update(self):
        """Read raw input data and convert it to a gamepad-compatible value."""
        # clamp raw input value to specified min/max
        value = min(max(self._source.value, self._min), self._max)

        # account for deadband
        if value < (self._raw_midpoint - self._deadband):
            value = value - self._min
        elif value > (self._raw_midpoint + self._deadband):
            value = value - self._min - (self._deadband * 2)
        else:
            value = self._db_range // 2

        # calculate scaled joystick-compatible value and clamp to +/- 127
        self._value = (
            min(max(value * 255 // self._db_range - 127, -127), 127) * self._invert
        )

        return self._value


class Hat:
    """Data source storage and value conversion for hat switch inputs."""

    # friendly names for angular positions
    U = 0
    UR = 1
    R = 2
    DR = 3
    D = 4
    DL = 5
    L = 6
    UL = 7
    IDLE = 8

    @property
    def value(self) -> int:
        """Return the current hat switch angular position value."""
        return self._value

    @property
    def active_low(self) -> bool:
        """Return ``True`` if the hat switch inputs are set to active low."""
        return self._active_low

    @property
    def up(self) -> bool:
        """Return the logical state of the up input."""
        return self._up.value != self._active_low

    @up.setter
    def up(self, state: bool) -> None:
        """Allow setting the logical up input state for VirtualInputs."""
        if not isinstance(self._up, VirtualInput):
            raise TypeError("Only VirtualInput source values can be set manually.")
        if self._active_low:
            state = not state
        self._up.value = state

    @property
    def down(self) -> bool:
        """Return the logical state of the down input."""
        return self._down.value != self._active_low

    @down.setter
    def down(self, state: bool) -> None:
        """Allow setting the logical down input state for VirtualInputs."""
        if not isinstance(self._down, VirtualInput):
            raise TypeError("Only VirtualInput source values can be set manually.")
        if self._active_low:
            state = not state
        self._down.value = state

    @property
    def left(self) -> bool:
        """Return the logical state of the left input."""
        return self._left.value != self._active_low

    @left.setter
    def left(self, state: bool) -> None:
        """Allow setting the logical left input state for VirtualInputs."""
        if not isinstance(self._left, VirtualInput):
            raise TypeError("Only VirtualInput source values can be set manually.")
        if self._active_low:
            state = not state
        self._left.value = state

    @property
    def right(self) -> bool:
        """Return the logical state of the right input."""
        return self._right.value != self._active_low

    @right.setter
    def right(self, state: bool) -> None:
        """Allow setting the logical right input state for VirtualInputs."""
        if not isinstance(self._right, VirtualInput):
            raise TypeError("Only VirtualInput source values can be set manually.")
        if self._active_low:
            state = not state
        self._right.value = state

    def __init__(
        self,
        up: Pin = None,
        down: Pin = None,
        left: Pin = None,
        right: Pin = None,
        active_low: bool = True,
    ) -> None:
        """Create a hat switch using the specified data sources."""
        self._up = self._initialize_source(up, active_low)
        self._down = self._initialize_source(down, active_low)
        self._left = self._initialize_source(left, active_low)
        self._right = self._initialize_source(right, active_low)
        self._active_low = active_low
        self._value = Hat.IDLE
        self.update()

    @staticmethod
    def _initialize_source(
        pin: Union[Pin, VirtualInput],
        active_low: bool,
    ) -> Union[DigitalInOut, VirtualInput]:
        """Configure an input as a GPIO pin or VirtualInput."""
        if isinstance(pin, Pin):
            source = DigitalInOut(pin)
            source.direction = Direction.INPUT
            if active_low:
                source.pull = Pull.UP
            else:
                source.pull = Pull.DOWN
            return source
        else:
            return VirtualInput(value=active_low)

    def update(self) -> int:
        """Update the angular position value based on discrete input states."""
        U = self.up
        D = self.down
        L = self.left
        R = self.right

        if U and R:
            self._value = Hat.UR
        elif U and L:
            self._value = Hat.UL
        elif U:
            self._value = Hat.U
        elif D and R:
            self._value = Hat.DR
        elif D and L:
            self._value = Hat.DL
        elif D:
            self._value = Hat.D
        elif L:
            self._value = Hat.L
        elif R:
            self._value = Hat.R
        else:
            self._value = Hat.IDLE
        return self._value
