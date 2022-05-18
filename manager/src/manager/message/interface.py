"""Module for the manager messages"""


from enum import Enum

from ..fiware import FIWARE
from . import ENTITY_ID

TYPE = "message"


class DESTINATION(Enum):
    """Enum class to store the possible message destinations"""

    ROBOTIC = f"{ENTITY_ID}.robotic"
    COLLABORATIVE = f"{ENTITY_ID}.collaborative"
    VISION = f"{ENTITY_ID}.vision"


class Messenger:
    """Class for managing manager messages to the FIWARE OCB"""

    def __init__(self, server_address: str) -> None:

        self.__fiware = FIWARE(server_addr=server_address)

    def new_message(self, destination: DESTINATION, message: str):
        """Creates a new message and attempts to upload it to the OCB

        Args:
            destination (DESTINATION): The destination node
            message (str): The message content

        Returns:
            bool: The operation success
        """
        message_dict = {"id": destination.value, "type": TYPE, "message": {"type": "Text", "value": message}}

        # first try to create a new entity
        success = self.__fiware.create_entity(message_dict)

        if not success:
            # if a new entity already exists, try to update the attributes
            message_dict = {"message": {"type": "Text", "value": message}}

            success = self.__fiware.update_entity(entity_id=destination.value, attrs=message_dict)

        return success

    def get_message(self, destination: DESTINATION) -> str:
        """Retrieves a message from the OCB

        Args:
            destination (DESTINATION): The destination the message should be retrieved from (ID)

        Returns:
            str: The message's content
        """

        message_dict = self.__fiware.get_entity(entity_id=destination.value)

        if message_dict is None:
            return ""

        attr_dict = message_dict.get("message")

        assert attr_dict is not None

        message_content = attr_dict.get("value")

        assert message_content is not None

        return message_content
