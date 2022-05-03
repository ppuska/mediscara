"""Module for structuring the data according to the NGSi V2 standard"""

from dataclasses import dataclass, field
from typing import Any

@dataclass
class NGSI:
    """Data class for storing the sensor data in the NGSI V2 format

    Raises:
        TypeError: If an invalid value is given for the temperature or the humidity
    """

    @dataclass
    class Field:
        """Data class for storing a single field for the NGSI document

        Raises:
            TypeError: If an invalid value is given
        """
        value: Any
        type: str = field(init=False)

        def __post_init__(self):
            if isinstance(self.value, float):
                self.type = "Float"

            elif isinstance(self.value, float):
                self.type = "String"

            else:
                raise TypeError(f"No type alias for type: {type(self.value)}")

    id: str
    type: str

    temperature: Field = field(default=Field(value=0.0))
    humidity: Field = field(default=Field(value=0.0))