"""This is a module for storing configuration files"""
from enum import Enum


class IPList(Enum):
    """Enum class for storing ip addresses"""
    MarkerIP = 'localhost'  # todo change to real IP
    Grafana = 'http://localhost:3003'
    CrateDB = 'http://host.docker.internal:4200'

    Robot2 = '192.168.0.22'


class PortList(Enum):
    """Enum class for storing ports"""
    Marker = 65432
    Robot2 = 65432


class SQLTableNames(Enum):
    """Enum class for storing SQL database table names"""
    CELL1 = 'sc1'
    CELL2 = 'sc2'
