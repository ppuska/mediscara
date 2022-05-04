"""Module to implement the sensor-FIWARE communication"""

import logging
import requests

class Comm:
    """Class to implement communication to the Orion Context Broker"""

    def __init__(self, server_address: str):
        self.__server_address = server_address

        
