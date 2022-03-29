from enum import Enum

from interfaces.msg import VisionControl, Robot2Control, MarkerStatus as Ms
from std_msgs.msg import Bool


class NodeList(Enum):
    """Enum class for storing the Nodes and their names in the system"""
    Robot1Node = 'robot1'
    Robot2Node = 'robot2'
    SensorNode = 'sensor'
    MarkerNode = 'marker'
    LaserNode = 'laser'
    HMINode = 'hmi'
    FIWARENode = "is_ros2"


class MessageList(Enum):
    """Enum class for storing message topics and their respective message types"""
    MarkerStatus = 'marker_status', Ms
    MarkerControl = 'marker_control', Bool
    Robot2Control = 'robot2_control', Robot2Control
    VisionControl = 'vision_control', VisionControl


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
