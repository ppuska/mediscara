"""Test module for the manager messages"""

from manager.message.interface import DESTINATION, Messenger

SERVER_ADDRESS = "25.18.161.28"


def test_messages():
    m = Messenger(server_address=SERVER_ADDRESS)

    assert m.new_message(destination=DESTINATION.COLLABORATIVE, message="Test message") is True

    print(m.get_message(destination=DESTINATION.COLLABORATIVE))


if __name__ == "__main__":
    test_messages()
