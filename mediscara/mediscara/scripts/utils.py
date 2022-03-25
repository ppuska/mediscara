import enum
from dataclasses import dataclass
from functools import wraps

from interfaces.msg import Error, MarkerStatus as Ms
from std_msgs.msg import Bool


class Debug:
    DEBUG = False

    @staticmethod
    def debug_method(func):
        """If this decorator is used, the method will only run if the DEBUG flag is set to True"""

        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            return result

        def dummy(*_, **__):
            pass

        if Debug.DEBUG:
            return wrapper

        else:
            return dummy


class NodeList(enum.Enum):
    """Enum class for storing the Nodes and their names in the system"""
    Robot1Node = 'robot1'
    Robot2Node = 'robot2'
    SensorNode = 'sensor'
    MarkerNode = 'marker'
    LaserNode = 'laser'
    HMINode = 'hmi'
    FIWARENode = "is_ros2"


class MessageList(enum.Enum):
    """Enum class for storing message topics and their respective message types"""
    MarkerStatus = 'marker_status', Ms
    MarkerControl = 'marker_control', Bool
    Robot2Control = 'robot_control', Bool  # todo implement correctly


class IPList(enum.Enum):
    """Enum class for storing ip addresses"""
    MarkerIP = 'localhost'  # todo change to real IP
    Grafana = 'http://localhost:3003'
    CrateDB = 'http://host.docker.internal:4200'

    Robot2 = '192.168.0.22'


class PortList(enum.Enum):
    """Enum class for storing ports"""
    Marker = 65432
    Robot2 = 65432


class SQLTableNames(enum.Enum):
    """Enum class for storing SQL database table names"""
    CELL1 = 'sc1'
    CELL2 = 'sc2'


@dataclass
class ErrorClass:
    error_code: int
    error_msg: str

    @classmethod
    def from_error_msg(cls, e: Error):
        return cls(error_msg=e.error_msg, error_code=e.error_code)
