"""This is a module for storing configuration files"""
from enum import Enum


class IPList(Enum):
    """Enum class for storing ip addresses"""

    MARKER_IP = "localhost"  # todo change to real IP
    GRAFANA = "http://localhost:3003"
    CRATE_DB = "http://host.docker.internal:4200"

    ROBOT2 = "192.168.0.22"


class PortList(Enum):
    """Enum class for storing ports"""

    MARKER = 65432
    ROBOT2 = 65432


class SQLTableNames(Enum):
    """Enum class for storing SQL database table names"""

    CELL1 = "sc1"
    CELL2 = "sc2"
