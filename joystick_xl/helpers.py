try:
    from typing import Union
except ImportError:
    pass


class VirtualInput:
    """Provide an object with a .value property to represent an input."""

    def __init__(self, value: Union[bool, int]) -> None:
        """Set initial .value property (True for buttons, 32768 for axes)."""
        self.value = value


class Axis:
    """Data source storage and scaling/deadband processing for an axis input."""

    @property
    def min(self) -> int:
        return self._min

    @property
    def max(self) -> int:
        return self._max

    @property
    def deadband(self) -> int:
        return self._deadband

    @property
    def value(self) -> int:
        return self._value

    def __init__(self, source, deadband: int = 0, min: int = 0, max: int = 65535):
        """Create an axis object using the specified input data source object."""
        if not hasattr(source, "value"):
            raise ValueError("Axis source must be an object with a 'value' attribute.")
        self._source = source
        self._deadband = deadband
        self._min = min
        self._max = max
        self._value = 0

        # calculate raw input midpoint and scaled deadband range
        self._raw_midpoint = self._min + ((self._max - self._min) // 2)
        self._db_range = self._max - self._min - (self._deadband * 2)

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
        self._value = min(max(value * 255 // self._db_range - 127, -127), 127)

        return self._value
