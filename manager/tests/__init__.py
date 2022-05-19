"""Init module for the tests"""

import sys

if sys.platform.startswith("win"):
    PING = "ping /n 1 "

else:
    PING = "ping -c 1 "
