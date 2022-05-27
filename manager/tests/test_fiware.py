"""Testing module for the interfaces module"""

import os

import pytest

from manager.fiware import FIWARE

from . import PING, SERVER_ADDR


def test_connection():
    """This method tests the init method of the fiware interface"""

    entity_id = "manager.message"
    entity_attrs = {"content": {"type": "Text", "value": "test message"}}
    entity_attrs_updated = {"content": {"type": "Text", "value": "test message2"}}

    entity = {"id": entity_id, "type": "Message", "content": entity_attrs.get("content")}

    try:
        f_connector = FIWARE("25.18.161.28")

    except ConnectionError:
        pytest.skip("Skipping connection error")

    f_connector.delete_entity(entity_id=entity_id)

    assert f_connector.create_entity(entity=entity) is True
    assert f_connector.update_entity(entity_id=entity_id, attrs=entity_attrs_updated) is True
    assert f_connector.delete_entity(entity_id=entity_id) is True


if __name__ == "__main__":
    test_connection()
