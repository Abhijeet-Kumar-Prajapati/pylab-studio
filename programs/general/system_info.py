"""
System Info
Category: Utility

Shows Python and OS information.

Example:
    version details
"""

import platform, sys


def main():
    """Entry point."""

    print("Python:", sys.version.split()[0])
    print("Platform:", platform.system(), platform.release())
    print("Machine:", platform.machine())


if __name__ == "__main__":
    main()
