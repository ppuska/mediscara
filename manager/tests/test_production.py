# pylint: skip-file

import logging
import pytest


from manager.production.interface import Production
from manager.production.model import Container, IndustialOrder
from manager.fiware import FIWARE

from . import SERVER_ADDR


def test_model():
    industrial_model = IndustialOrder()
    industrial_model.count = 10
    industrial_model.incubator_type = "incubator_type1"

    assert industrial_model.to_ngsi() == {
        "type": "order.industrial",
        "value": {
            "incubator_type": {"type": "Text", "value": "incubator_type1"},
            "count": {"type": "Number", "value": 10},
        },
    }


@pytest.fixture
def container():
    model1 = IndustialOrder()
    model1.count = 100
    model1.incubator_type = "type1"
    model2 = IndustialOrder()
    model2.count = 15
    model2.incubator_type = "type2"
    container = Container(order_list=[model1, model2])

    return container


@pytest.fixture
def clean(container):
    """Clears the entity from the OCB"""
    connector = FIWARE(server_addr=SERVER_ADDR)
    assert isinstance(container, Container)
    removed = connector.delete_entity(container.container_id)

    if removed:
        logging.info("Cleaned, entity removed")


def test_container(container):
    assert container.to_ngsi() == {
        "id": "order.industrial.container",
        "type": "order.industrial.container",
        "order_list": {
            "type": "StructuredValue",
            "value": [
                {
                    "type": "order.industrial",
                    "value": {
                        "incubator_type": {"type": "Text", "value": "type1"},
                        "count": {"type": "Number", "value": 100},
                    },
                },
                {
                    "type": "order.industrial",
                    "value": {
                        "incubator_type": {"type": "Text", "value": "type2"},
                        "count": {"type": "Number", "value": 15},
                    },
                },
            ],
        },
    }


def test_production(clean):
    order1 = IndustialOrder()
    order1.count = 100
    order1.incubator_type = "type1"
    order2 = IndustialOrder()
    order2.count = 15
    order2.incubator_type = "type2"

    p = Production(SERVER_ADDR)
    assert p.new_production_order(order1) is True
    assert p.new_production_order(order2) is True


if __name__ == "__main__":
    test_model()
