"""Test module for the manager messages"""

import os

import pytest

from manager.message.interface import DESTINATION, Messenger

from . import PING

SERVER_ADDRESS = "25.18.161.28"


@pytest.mark.skipif(os.system(PING + SERVER_ADDRESS) != 0, reason="Unable to ping server")
def test_messages():
    try:
        m = Messenger(server_address=SERVER_ADDRESS)

    except ConnectionError:
        pytest.skip("Skipping connection error")

    assert m.new_message(destination=DESTINATION.COLLABORATIVE, message="Test message") is True

    print(m.get_message(destination=DESTINATION.COLLABORATIVE))


if __name__ == "__main__":
    test_messages()
