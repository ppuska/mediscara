"""Module for storing interface classes"""

import logging
from enum import Enum

import requests


class StatusCodes(Enum):
    """Enum class to store the HTTP request response status codes"""

    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    NOT_FOUND = 404
    UNPROCESSABLE = 422


class FIWARE:
    """Communication class for interfacing with the Orion Context Broker"""

    OCB_PORT = 1026

    def __init__(self, server_addr: str) -> bool:
        """Initializes the communication to the FIWARE OCB

        Args:
            server_addr (str): The IPv4 address of the OCB server

        Raises:
            ConnectionError: If the connection cannot be established
        """
        self.__server_address = f"{server_addr}:{self.OCB_PORT}"

        # test the connection to the server
        try:
            response = requests.get(f"https://{self.__server_address}/v2")

            if response.status_code == StatusCodes.OK.value:
                logging.info("Communication initialized, server online")

            else:
                logging.info("Communication initalized, server unreachable (response %i)", response.status_code)

        except requests.exceptions.ConnectionError as error:
            logging.error("Failed to establish connection")
            raise ConnectionError from error

    def add_command(self):
        """Adds a command"""

    def remove_command(self):
        """removes a command"""
