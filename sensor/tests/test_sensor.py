"""Module to test the sensor class"""

import time
from sensor.temp_hum import DHTSensor
from sensor.config import DHT_PIN

def test_sensor():
    sensor = DHTSensor(pin_number=DHT_PIN)
    try:
        while True:
            print(sensor.read_data())
            time.sleep(1)

    except KeyboardInterrupt:
        pass

def main():
    test_sensor()


if __name__ == "__main__":
    main()