"""Module for processing the sensor data in the cell"""

from time import sleep
try:
    from sensor.temp_hum import DHTSensor
    from sensor import shock
    from sensor.ngsi import NGSI

except ImportError:
    from temp_hum import DHTSensor
    import shock
    from ngsi import NGSI

UPDATE_INTERVAL = 5

class Sensor:
    """Class for managing sensor data in the cell"""

    def __init__(self, dht_pin: int) -> None:
        # dht sensor
        self.__dht = DHTSensor(dht_pin)

        # shock sensor
        shock.initialize(pin_shock=15, callback=self.shock_sensor_callback)
        self.__shock = False

        self.__data = NGSI(id_="sensor_data", type_="Sensor")

    def shock_sensor_callback(self, _: int):
        """Callback method for the shock sensor"""
        self.__shock = True

    def update(self):
        """Updates the sensor data and returns it

        Returns:
            dict: The sensor data formatted to the NGSI v2 format
        """
        dht_data = self.__dht.read_data()

        result = self.__data

        result.add_attribute("temperature", dht_data.temperature_c)
        result.add_attribute("humidity", dht_data.humidity)

        result.add_attribute("shock", self.__shock)

        self.__shock = False

        return result.to_dict()


def main():
    sensor = Sensor(14)

    try:
        while True:
            print(sensor.update())
            sleep(UPDATE_INTERVAL)


    except KeyboardInterrupt:
        print("\nExiting")


if __name__ == "__main__":
    main()
