"""
Compile and bundle JoystickXL for release on Github.

Yes, there is a nasty bit of path manipulation to allow importing of joystick_xl
modules from this folder.  Sorry. :P
"""

import subprocess
import sys
import zipfile
from pathlib import Path
from typing import List

CP_VERSIONS = [8, 9]
JXL_PATH = Path(__file__).parent.parent.parent

try:
    sys.path.append(str(JXL_PATH))
    from joystick_xl import __version__ as version
except ImportError:
    print("*** ERROR: Can't import joystick_xl modules. ***")
    sys.exit()


def cleanup(file_patterns: List[str], folder: Path = JXL_PATH / "joystick_xl") -> None:
    """Remove files matching the specified patterns from the module folder."""
    for pattern in file_patterns:
        for file in list((JXL_PATH / "joystick_xl").glob(pattern)):
            file.unlink()


files = list((JXL_PATH / "joystick_xl").glob("*.py"))

if not files:
    print("*** ERROR: Could not locate joystick_xl .py files")
    sys.exit()

print(f"Creating JoystickXL {version} bundles for CircuitPython versions {CP_VERSIONS}")

for v in CP_VERSIONS:
    try:
        cleanup(["*.mpy"])
        for f in files:
            command = [f"mpy-cross{v}", f]
            process = subprocess.Popen(command)
            process.wait()
        bundle_file = Path(__file__).parent / f"joystick_xl_{version}_cp{v}.zip"
        bundle_files = list((JXL_PATH / "joystick_xl").glob("*.mpy"))
        bundle_files.append(JXL_PATH / "README.rst")
        bundle_files.append(JXL_PATH / "LICENSE")
        with zipfile.ZipFile(bundle_file, "w") as zip_file:
            for f in bundle_files:
                zip_file.write(f, f"joystick_xl/{f.name}")
        cleanup(["*.mpy"])
    except FileNotFoundError:
        print(f"*** ERROR: mpy-cross{v}.exe not found, skipping CircuitPython {v}")
    print(f"+ Created {bundle_file.name} for CircuitPython {v}")
