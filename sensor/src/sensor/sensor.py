"""Module for processing the sensor data in the cell"""

from time import sleep
import logging

from sensor.temp_hum import DHTSensor
from sensor import shock
from sensor.ngsi import NGSI
from sensor.communication import Comm

UPDATE_INTERVAL = 5


class Sensor:
    """Class for managing sensor data in the cell"""

    ID = "sensor_data"

    def __init__(self, dht_pin: int, server_address: str) -> None:
        # dht sensor
        self.__dht = DHTSensor(dht_pin)

        # shock sensor
        shock.initialize(pin_shock=15, callback=self.shock_sensor_callback)
        self.__shock = False

        self.__data = NGSI(id_=Sensor.ID, type_="Sensor")

        # communication
        try:
            self.__comm = Comm(server_address)

        except ConnectionError:
            logging.info("Could not initalize communication, exiting")
            exit()

        # check if the OCB has the entity already
        if self.__comm.get_entity(self.ID) is None:
            logging.debug("Entity does not exist in Orion Context Broker")
            self.__comm.create_entity(json=self.__data.to_dict())

        else:
            logging.debug("Entity exists in Orion Context Broker")

    def shock_sensor_callback(self, _: int):
        """Callback method for the shock sensor"""
        self.__shock = True

    def update(self):
        """Updates the sensor data and returns it

        Returns:
            dict: The sensor data formatted to the NGSI v2 format
        """
        # calculate the sensor data results
        dht_data = self.__dht.read_data()

        result = self.__data

        result.add_attribute("temperature", dht_data.temperature_c)
        result.add_attribute("humidity", dht_data.humidity)

        result.add_attribute("shock", self.__shock)

        self.__shock = False

        # upload the data to the OCB
        self.__comm.update_entity(Sensor.ID, result.to_dict(header=False))

        return result.to_dict()
