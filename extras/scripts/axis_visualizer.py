"""
Display a graph that shows axis output values across the range of input values.

Yes, there is a nasty bit of path manipulation to allow importing of joystick_xl
modules from this folder.  Sorry. :P
"""

# Adjust the min/max/deadband values to suit your test case.
min = 5000
max = 64535
deadband = 2500

# nasty path manipulation
import os  # noqa: E402
import sys  # noqa: E402

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

try:
    from joystick_xl.inputs import Axis
except ImportError:
    print("*** ERROR: Can't import joystick_xl modules. ***")
    sys.exit()

try:
    from matplotlib import pyplot as plt
except ImportError:
    print("*** ERROR: matplotlib is required to display graphs. ***")

# readability constants
AXIS = 0
OUTPUT = 1
NODB = 0
NORMAL = 1
INVERTED = 2

# generate axis data
input = [i for i in range(65536)]
axes = [
    [Axis(min=min, max=max), []],
    [Axis(deadband=deadband, min=min, max=max, invert=False), []],
    [Axis(deadband=deadband, min=min, max=max, invert=True), []],
]
for i in input:
    for a in axes:
        a[AXIS].source_value = i
        a[OUTPUT].append(a[AXIS]._update())

# normal axis
plt.plot(input, axes[NORMAL][OUTPUT], color="blue", zorder=1.0)

# inverted axis
plt.plot(input, axes[INVERTED][OUTPUT], color="orange", zorder=0.9)

# reference line accounting for min/max but ignoring deadband
plt.plot(input, axes[NODB][OUTPUT], ":", color="lightgrey", zorder=0.1)

# minimum line
plt.axvline(x=min, color="lightgrey", linestyle=":", zorder=0.1)

# maximum line
plt.axvline(x=max, color="lightgrey", linestyle=":", zorder=0.1)

# center point accounting for min/max
plt.axvline(
    x=axes[NODB][AXIS]._raw_midpoint, color="lightgrey", linestyle=":", zorder=0.1
)

# labels and titles
plt.title("Processed Axis Output over Entire Input Range")
plt.xlabel("Raw Input Value (16-bit)")
plt.xticks([0, 8192, 16384, 24576, 32768, 40960, 49152, 57344, 65535])
plt.ylabel("Processed Axis Value (8-bit)")
plt.legend(["Normal", "Inverted"])

# draw it!
plt.show()
