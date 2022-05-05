"""Module to test the sensor class"""

from sensor.sensor import Sensor

def test_sensor():
    sensor = Sensor(14, server_address="localhost:1025")


def main():
    test_sensor()


if __name__ == "__main__":
    main()