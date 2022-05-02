"""Module for structuring the data according to the NGSi V2 standard"""

from dataclasses import fields, asdict, is_dataclass
from typing import Any

class NGSI:
    """Data class for storing the sensor data in the NGSI V2 format
    """

    ID = "id"
    TYPE = "type"
    VALUE = "value"

    NUMBER = "Number"
    BOOL = "Boolean"
    STRING = "String"

    def __init__(self, id_: str, type_: str):
        self.__id = id_
        self.__type = type_

        self.__attributes = list()

    def __str__(self):
        return str(self.to_dict())

    def add_attribute(self, attribute_name: str, attribute: Any):
        """Add a field to the NGSI object

        Args:

        """

        self.__attributes.append((attribute_name, attribute))

        return self

    def to_dict(self):
        """Returns the object as a dict"""
        result = {}

        result[NGSI.ID] = self.__id
        result[NGSI.TYPE] = self.__type

        for attr_name, attr in self.__attributes:
            attribute_dict = {}  # create a dictionary for each attribute

            if is_dataclass(attr):

                attr_fields = fields(attr)  # get the fields of the dataclass
                value_dict = asdict(attr)

                for field in attr_fields:
                    if field.type == float or field.type == int:
                        data_type = NGSI.NUMBER

                    elif field.type == bool:
                        data_type = NGSI.BOOL

                    elif field.type == str:
                        data_type = NGSI.STRING

                    else:
                        raise TypeError(f"Unsupported type of {field.type}")

                    attribute_dict[field.name] = {
                        NGSI.TYPE: data_type,
                        NGSI.VALUE: value_dict[field.name]
                    }

            else:
                if isinstance(attr, float) or isinstance(attr, int):
                    data_type = NGSI.NUMBER

                elif isinstance(attr, bool):
                    data_type = NGSI.BOOL

                elif isinstance(attr, str):
                    data_type = NGSI.STRING

                else:
                    raise TypeError(f"Unsupported type of {field.type}")

                attribute_dict = {
                    NGSI.TYPE: data_type,
                    NGSI.VALUE: attr
                }

            result[attr_name] = attribute_dict

        return result