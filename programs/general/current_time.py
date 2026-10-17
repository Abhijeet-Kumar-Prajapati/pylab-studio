"""
Current Time
Category: Utility

Shows the current date and time.

Example:
    live clock
"""

import datetime


def main():
    """Entry point."""

    now = datetime.datetime.now()
    print("Date:", now.strftime("%Y-%m-%d"))
    print("Time:", now.strftime("%H:%M:%S"))
    print("Full:", now.strftime("%A, %d %B %Y %H:%M:%S"))


if __name__ == "__main__":
    main()
