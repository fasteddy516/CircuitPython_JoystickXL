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

    def __init__(self, source, deadband: int = 0, min: int = 0, max: int = 65535):
        """Create an axis object using the specified input data source object."""
        if not hasattr(source, "value"):
            raise ValueError("Axis source must be an object with a 'value' attribute.")
        self.source = source
        self.deadband = deadband
        self.min = min
        self.max = max
        self.value = 0

    def update(self):
        """Read raw input data and convert it to a gamepad-compatible value."""
        # clamp raw input value to specified min/max
        value = min(max(self.source.value, self.min), self.max)

        # calculate raw input midpoint and scaled deadband range
        raw_midpoint = self.min + ((self.max - self.min) // 2)
        db_range = self.max - self.min - (self.deadband * 2)

        # account for deadband
        if value < (raw_midpoint - self.deadband):
            value = value - self.min
        elif value > (raw_midpoint + self.deadband):
            value = value - self.min - (self.deadband * 2)
        else:
            value = db_range // 2

        # calculate scaled gamepad-compatible value and clamp to +/- 127
        self.value = min(max(value * 255 // db_range - 127, -127), 127)

        return self.value
