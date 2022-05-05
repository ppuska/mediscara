from time import sleep

from sensor.sensor import Sensor
from sensor.config import SERVER_ADDRESS, UPDATE_INTERVAL


def main():
    sensor = Sensor(14, SERVER_ADDRESS)

    try:
        while True:
            print(sensor.update())
            sleep(UPDATE_INTERVAL)

    except KeyboardInterrupt:
        print("\nExiting")


if __name__ == "__main__":
    main()
