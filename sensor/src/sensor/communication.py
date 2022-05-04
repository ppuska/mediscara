"""Module to implement the sensor-FIWARE communication"""

import logging
import requests
from enum import Enum

class Comm:
    """Class to implement communication to the Orion Context Broker"""

    class StatusCodes(Enum):
        """Enum class to store the HTTP request response status codes"""
        OK = 200
        CREATED = 201
        NO_CONTENT = 204
        NOT_FOUND = 404
        UNPROCESSABLE = 422


    def __init__(self, server_address: str):
        self.__server_address = server_address

        try:

            response = requests.get(f"http://{self.__server_address}/v2")

            if response.status_code == Comm.StatusCodes.OK.value:
                logging.info("Communication initialized, server online")

            else:
                logging.warning("Communication initialized, server offline (response: %x)", response.status_code)

        except requests.exceptions.ConnectionError:
            logging.fatal("Failed to establish connection to server")
            raise ConnectionError()

    def get_entity(self, entity_id: str):
        """Tries to get the entity with the given id from the OCB"""

        response = requests.get(f"http://{self.__server_address}/v2/entities/{entity_id}")

        if response.status_code == Comm.StatusCodes.NOT_FOUND.value:
            return None

        else:
            return response.json()

    def create_entity(self, json: dict) -> bool:
        """Creates the entity with the given parameters"""

        response = requests.post(f"http://{self.__server_address}/v2/entities", json=json)

        if response.status_code == Comm.StatusCodes.CREATED.value:
            return True

        else:
            logging.debug("Unable to create entity: (%x) [%s]", response.status_code, response.content)
            return False

    def update_entity(self, entity_id: str, json: dict) -> bool:
        """Updates the entity

        Args:
            entity_id (str): the id of the entity to be updated
            json (dict): the attributes of the entity

        Returns:
            bool: True if the operation was successful
        """
        response = requests.patch(f'http://{self.__server_address}/v2/entities/{entity_id}/attrs',
                                  json=json
                                  )

        if response.status_code == Comm.StatusCodes.NO_CONTENT.value:
            return True

        else:
            logging.debug("Failed to update entity: %s, response: %s (%x)", entity_id, response.content, response.status_code)

    def delete_entity(self, entity_id: str) -> bool:
        """Deletes the entity"""
        response = requests.delete(f"http://{self.__server_address}/v2/entities/{entity_id}")

        if response.status_code == Comm.StatusCodes.NO_CONTENT.value:
            return True

        else:
            logging.debug("Failed to delete entity: %s, response was %x: %s", entity_id, response.status_code, response.content)
            return False
