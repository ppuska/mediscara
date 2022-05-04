from sensor.ngsi import NGSI
from sensor.temp_hum import DHTSensor

def test():
    ngsi = NGSI(id_="sensor_data", type_="Sensor").add_attribute("temperature", DHTSensor.Data(humidity=15, temperature_c=23))
    print(ngsi.to_dict())

def test_no_header():
    ngsi = NGSI(id_="sensor_data", type_="Sensor").add_attribute("temperature", DHTSensor.Data(humidity=15, temperature_c=23))
    print(ngsi.to_dict(header=False))

if __name__ == "__main__":
    test()
    test_no_header()
