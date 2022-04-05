"""Module for the Sensor Node in the cell"""
import json
from random import random
import sys
import time
import logging
from dataclasses import dataclass, field
import re

import requests
import simplejson

from ngsi import DataModel, JSONContent


@dataclass
class SensorData(DataModel):
    """Class for managing sensor data in the cell"""

    content: JSONContent = field(default=JSONContent("temperature", "humidity"))

    def update(self):
        self.content.temperature.value = 23 + random() * 5
        self.content.humidity.value = 65 + random() * 10

class FiwareCommunicator:
    """Class for communicating with the FIWARE Orion Context Broker"""

    CB_URL = "http://localhost:1026"

    def __init__(self) -> None:
        logging.basicConfig(level=logging.INFO)

        self.sensor = SensorData()
        self.sensor.update()

        # check if entity exists
        result = requests.get(url=f"{self.CB_URL}/v2/entities/{self.sensor.header.id}")

        if result.status_code == 404: # entity not found
            sensor_json = self.sensor.to_json()
            logging.info("Entity not found, creating new, payload: %s", sensor_json)
            result = requests.post(url=f"{self.CB_URL}/v2/entities",
                                   json=sensor_json
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

                    result = re.search(string=self.sensor.header.id, pattern=id_pattern)

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
                    "idPattern": f"{self.sensor.header.id}"
                }],
                "condition": {
                    "attrs": self.sensor.field_names(with_header=False)
                }
            },
            "notification": {
                "http": {
                    "url": "http://host.docker.internal:8668/v2/notify"
                },
                "attrs": self.sensor.field_names(with_header=False)
            }
        }

        response = requests.post(url=f"{self.CB_URL}/v2/subscriptions",
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(data))

        if response.status_code == 201:  # created
            logging.info("Subscription created")

        else:
            logging.warning("Subscription creation failed")

    def update(self):
        """Updates the sensor value in the OCB"""
        self.sensor.update()  # fetch sensor data

        response = requests.patch(url=f"{self.CB_URL}/v2/entities/{self.sensor.header.id}/attrs",
                                  json=self.sensor.to_json(with_header=False)
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
            print(f"Current temperature: {self.sensor.content.temperature.value}" \
                  f"°C, Current humidity: {self.sensor.content.humidity.value} %H",
                  end="\r"
                  )



def main():
    fc = FiwareCommunicator()
    try:
        fc.begin()
    except KeyboardInterrupt:
        logging.info("Ctrl+C, stopping")

if __name__ == "__main__":
    main()
