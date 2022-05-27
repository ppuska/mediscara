"""Init module for the tests"""

import sys
import os

import pytest

if sys.platform.startswith("win"):
    PING = "ping /n 1 "

else:
    PING = "ping -c 1 "

SERVER_ADDR = "25.18.161.28"

if os.system(f"{PING} {SERVER_ADDR} >nul") != 0:
    # skip the module if we cannot ping the server
    pytest.skip(reason="Unable to ping server", allow_module_level=True)
