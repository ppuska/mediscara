from dataclasses import asdict
from sensor.ngsi import NGSI

def test():
    ngsi = NGSI(id="sensor_data", type="Sensor")
    print(asdict(ngsi))


if __name__ == "__main__":
    test()
