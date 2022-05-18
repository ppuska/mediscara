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
            response = requests.get(f"http://{self.__server_address}/v2")

            if response.status_code == StatusCodes.OK.value:
                logging.info("Communication initialized, server online")

            else:
                logging.info("Communication initalized, server unreachable (response %i)", response.status_code)

        except requests.exceptions.ConnectionError as error:
            logging.error("Failed to establish connection")
            raise ConnectionError from error

    def create_entity(self, entity: dict) -> bool:
        """Creates an entity in the OCB

        Args:
            entity (dict): The JSON representation formatted as NGSIv2

        Returns:
            bool: Whether the operation was successful or not
        """

        response = requests.post(f"http://{self.__server_address}/v2/entities", json=entity)

        if response.status_code == StatusCodes.CREATED.value:
            return True

        logging.debug("Could not create new entity (response: %s)", response.content)
        return False

    def get_entity(self, entity_id: str) -> dict or None:
        """Return the entity with the given id from the OCB

        Args:
            entity_id (str): The id of the entity

        Returns:
            dict or None: The JSON representation of the entity, or None if the entity was not found
        """

        response = requests.get(f"http://{self.__server_address}/v2/entities/{entity_id}")

        if response.status_code == StatusCodes.NOT_FOUND.value:
            logging.debug("%s not found.", entity_id)
            return None

        return response.json()

    def update_entity(self, entity_id: str, attrs: dict) -> bool:
        """Updates the entity with the given id in the OCB

        Args:
            entity_id (str): The ID of the entity
            attrs (dict): the attributes of the entity to be updated

        Returns:
            bool: Whether the operation was successful
        """
        response = requests.patch(f"http://{self.__server_address}/v2/entities/{entity_id}/attrs", json=attrs)

        if response.status_code == StatusCodes.NO_CONTENT.value:
            return True

        logging.debug("Unable to update entity '%s'. (response %s)", entity_id, response.content)
        return False

    def delete_entity(self, entity_id: str):
        """Deletes the entity from the OCB

        Args:
            entity_id (str): The ID of the entity

        Returns:
            _type_: Whether the operation was successful or not
        """
        response = requests.delete(f"http://{self.__server_address}/v2/entities/{entity_id}")

        if response.status_code == StatusCodes.NO_CONTENT.value:
            return True

        logging.debug("Unable to delete entity '%s'. (response %s'", entity_id, response.content)
        return False
