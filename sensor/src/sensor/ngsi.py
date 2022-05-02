"""Module for structuring the data according to the NGSi V2 standard"""

from dataclasses import dataclass, fields, asdict

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

    def add_attribute(self, attribute_name: str, attribute: dataclass):
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

            result[attr_name] = attribute_dict

        return result