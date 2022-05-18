"""Testing module for the interfaces module"""

import logging

from manager.interfaces import FIWARE


def test_connection():
    """This method tests the init method of the fiware interface"""
    try:
        f_connector = FIWARE("25.18.161.28")

    except ConnectionError:
        logging.fatal("Connection error")


if __name__ == "__main__":
    test_connection()
