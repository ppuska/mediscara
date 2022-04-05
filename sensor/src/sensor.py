"""Module for the Sensor Node in the cell"""
import dataclasses
import json
import random
import sys
import time
from typing import Any, ClassVar, List
import logging
from dataclasses import dataclass, field
import math
import re

import requests
import simplejson

@dataclass
class JSONField:
    """Class for storing a single JSON Field"""
    type: str
    value: Any

@dataclass
class Sensor:
    """Class for managing sensor data in the cell"""

    id: str = "sensor_data"
    type: str = "Sensor"

    temperature: JSONField = field(default=JSONField(type="Number", value=0.0))
    humidity: JSONField = field(default=JSONField(type="Number", value=0.0))

    c: ClassVar[float] = random.random()

    @classmethod
    def field_names(cls, with_header: bool = True) -> List[str]:
        """Returns the field names of this class"""
        if with_header:
            return [field_.name for field_ in dataclasses.fields(cls)]

        result = list()
        for field_ in dataclasses.fields(cls):
            if field_.name != "id" or field_.name != "type":
                result.append(field_.name)

        return result

    def to_json(self, with_header: bool = True) -> str:
        """Returns the class as a JSON formatted string"""
        data = dataclasses.asdict(self)
        if with_header:
            return json.dumps(data)

        else:
            del data["id"]
            del data["type"]

            return json.dumps(data)


    def get_data(self):
        """Fetches the data from the sensor"""
        self.temperature.value = (math.sin(self.c) + 1) * 50
        self.humidity.value = (math.cos(self.c) + 1) * 100

        self.c += 0.1

class FiwareCommunicator:
    """Class for communicating with the FIWARE Orion Context Broker"""

    CB_URL = "http://localhost:1026"

    def __init__(self) -> None:
        logging.basicConfig(level=logging.DEBUG)

        self.sensor = Sensor()
        self.sensor.get_data()

        # check if entity exists
        result = requests.get(url=f"{self.CB_URL}/v2/entities/{self.sensor.id}")

        if result.status_code == 404: # entity not found
            sensor_json = self.sensor.to_json()
            logging.info("Entity not found, creating new, payload: %s", sensor_json)
            result = requests.post(url=f"{self.CB_URL}/v2/entities",
                                   data=sensor_json,
                                   headers={"content-Type": "application/json"}
                                   )
            if result.status_code == 201:  # created == success
                logging.info("Operation successful")

            else:
                if result.status_code != 204:
                    logging.fatal("Could not create entity: %s", result.json())

                else:
                    logging.fatal("Could not create entity")
                sys.exit()

        else:
            logging.info("Entity found")

        # check if subscription exists
        response = requests.get(f"{self.CB_URL}/v2/subscriptions")

        try:
            data = response.json()

            for subscription in data:

                assert isinstance(subscription, dict)

                subject = subscription["subject"]
                entities = subject["entities"]

                for entity in entities:
                    id_pattern = entity["idPattern"]

                    result = re.search(string=self.sensor.id, pattern=id_pattern)

                    if result is not None:
                        return

            logging.info("No subscription found, creating one")
            self.create_subscription()


        except KeyError:
            print("No subscription")

        except simplejson.JSONDecodeError:
            logging.error("Server response error")


    def create_subscription(self):
        """Creates a subscription for the sensor data in the OCB"""
        data = {
            "description": "Notify QuantumLeap that sensor values are updated",
            "subject": {
                "entities": [{
                    "idPattern": f"{self.sensor.id}"
                }],
                "condition": {
                    "attrs": self.sensor.field_names()
                }
            },
            "notification": {
                "http": {
                    "url": "http://host.docker.internal:8668/v2/notify"
                },
                "attrs": self.sensor.field_names(with_header=False)
            }
        }

        print(data)

        response = requests.post(url=f"{self.CB_URL}/v2/subscriptions",
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(data))

        if response.status_code == 201:  # created
            logging.info("Subscription created")

        else:
            logging.warning("Subscription creation failed")

    def update(self):
        """Updates the sensor value in the OCB"""
        self.sensor.get_data()  # fetch sensor data

        response = requests.patch(url=f"{self.CB_URL}/v2/entities/{self.sensor.id}/attrs",
                                  headers={"Content-Type": "application/json"},
                                  data=self.sensor.to_json(with_header=False)
                                  )

        if response.status_code == 204:  # no content == success
            logging.debug("Update successful")

        else:
            logging.warning("Update unsuccessful")

    def begin(self):
        """Begins the update of the sensor data"""
        while True:
            time.sleep(5)

            self.update()



def main():
    fc = FiwareCommunicator()
    try:
        fc.begin()
    except KeyboardInterrupt:
        logging.info("Ctrl+C, stopping")

if __name__ == "__main__":
    main()
