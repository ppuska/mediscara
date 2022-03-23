"""Module for processing the sensor data in the cell"""

from pigpio_dht import DHT11

from sensor.ngsi import NGSI

class Sensor:
    """Class for managing sensor data in the cell"""

    def __init__(self, dht_pin: int) -> None:
        self.__dht = DHT11(dht_pin)

        self.__data = NGSI(id="sensor_data", type="Sensor")



    def update(self):
        pass

    def to_json(self):
        pass
