"""Module to store NGSI v2 data"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import dataclasses
from random import random
from typing import Any, List

@dataclass
class JSONField:
    """Class for storing a single JSON Field"""
    type: str
    value: Any

    @classmethod
    def number_field(cls, value: Any = 0.0):
        """Creates a class with the 'Number' field"""
        return cls(type="Number", value=value)


@dataclass
class JSONHeader:
    """Class for representing the id and type in the NGSI v2 data model"""

    id: str = "sensor_data"
    type: str = "Sensor"

@dataclass
class JSONContent:
    """Class for representing the content of the NGSI v2 data model"""

    def __init__(self, *fields: str) -> None:
        fields_constructor = list()
        for field_ in fields:
            fields_constructor.append((field_, JSONField, field(default=JSONField.number_field())))

        self.__class__ = dataclasses.make_dataclass(cls_name=JSONContent.__name__,
                                                    fields=fields_constructor
                                                    )


@dataclass
class DataModel(ABC):
    """Data class for representing the NGSI v2 data model"""
    header: JSONHeader = field(default=JSONHeader())
    content: JSONContent = field(default=JSONContent())

    def __str__(self) -> str:
        return f"{self.to_json()}"

    @classmethod
    def field_names(cls, with_header: bool = True) -> List[str]:
        """Returns the field names of the content and the header if specified

        Args:
            with_header (bool, optional): Whether to return the header field names or not. Defaults to True.

        Returns:
            List[str]: The list of field names
        """
        result = list()
        result.extend([field.name for field in dataclasses.fields(cls.content)])  # extend the list with the field names of the content

        if with_header:
            result.extend([field.name for field in dataclasses.fields(cls.header)])  # extend the list with the field names of the header

        return result

    @abstractmethod
    def update(self):
        """Updates the content values in the field"""

    def to_json(self, with_header: bool = True):
        """Converts the object to a JSON formatted dict

        Args:
            with_header (bool, optional): Whether to include the header or not. Defaults to True.
        """

        content_dict = dataclasses.asdict(self.content)

        if not with_header:
            return content_dict

        header_dict = dataclasses.asdict(self.header)
        return {**header_dict, **content_dict}  # this merges the two dicts together
