"""Module for reading the temperature and humidity values from the sensor"""
from dataclasses import dataclass, field
from time import time
import logging

from pigpio_dht import DHT11


class DHTSensor:
    """Class for interfacing with the DHT sensor"""
    __TEMP_C = "temp_c"
    __TEMP_F = "temp_f"
    __HUMIDITY = "humidity"
    __VALID = "valid"

    @dataclass
    class Data:
        """Dataclass for storing sensor data (temperature and humidity)"""
        temperature_c: float = field(default=0.0)
        temperature_f: float = field(default=0.0)

        humidity: float = field(default=0.0)
        valid: bool = field(default=False)


    def __init__(self, pin_number: int) -> None:
        self.__sensor = DHT11(pin_number)

        self.__last_read = time()

    def read_data(self) -> Data:
        """Reads the temperature and humidity data from the sensor

        Returns:
            SensorData: Dataclass of the returned elements
        """
        data = DHTSensor.Data()

        if time() - self.__last_read > 1:
            try:
                result = self.__sensor.read()

                data.temperature_c = result[self.__TEMP_C]
                data.temperature_f = result[self.__TEMP_F]
                data.humidity = result[self.__HUMIDITY]
                data.valid = result[self.__VALID]

                self.__last_read = time()

            except TimeoutError:
                logging.warning("Sensor timed out")

        return data


def main():
    sensor = DHTSensor(14)
    try:
        while True:
            data = sensor.read_data()
            if data.valid:
                print(data)

    except KeyboardInterrupt:
        print("\nExiting")


if __name__ == "__main__":
    main()
