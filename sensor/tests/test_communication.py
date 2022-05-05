"""Module to test the communication scripts"""

from sensor.communication import Comm

ENTITY_ID = "temp"
ENTITY = {
        "id": ENTITY_ID,
        "type": "None"
        }

def test_init():
    c = Comm(server_address="localhost:1026")
    del c

def test_get_entity():
    c = Comm(server_address="localhost:1026")

    c.get_entity("sensor_data")

def test_create_entity():
    c = Comm(server_address="localhost:1026")

    return c.create_entity(ENTITY)

def test_delete_entity():
    c = Comm(server_address="localhost:1026")

    return c.delete_entity(ENTITY_ID)

def main():
    test_init()
    print(f"{test_get_entity()=}")
    print(f"{test_create_entity()=}")
    print(f"{test_delete_entity()=}")

if __name__ == "__main__":
    main()
