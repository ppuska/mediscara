import dataclasses
from src.ngsi import DataModel, JSONContent

def display_json_content():
    jc = JSONContent("temperature", "humidity")
    print(dataclasses.asdict(jc))

if __name__ == "__main__":
    # display_json()
    # display_field_names()
    display_json_content()
