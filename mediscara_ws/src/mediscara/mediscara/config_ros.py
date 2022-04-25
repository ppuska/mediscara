"""This is a module for setting and storing ROS2 related configuration data"""
from enum import Enum

from interfaces.msg import KPIC1 as kpi_c1, KPIC2 as kpi_c2, VisionControl as Vc, MarkerStatus as Ms
from interfaces.msg import Robot2Status as r2s, Robot2Control as r2c
from std_msgs.msg import Bool

class NodeList(Enum):
    """Enum class for storing the Nodes and their names in the system"""
    Robot1Node = 'robot1'
    Robot2Node = 'robot2'
    SensorNode = 'sensor'
    MarkerNode = 'marker'
    LaserNode = 'laser'
    VisionNode = 'vision'
    HMINode = 'hmi'
    FIWARENode = "is_ros2"


class MessageList(Enum):
    """Enum class for storing message topics and their respective message types"""
    MarkerStatus = 'marker_status', Ms
    MarkerControl = 'marker_control', Bool
    Robot2Status = 'robot2_status', r2s
    Robot2Control = 'robot2_control', r2c
    VisionControl = 'vision_control', Vc
    KPIC1 = 'kpi_cell1', kpi_c1
    KPIC2 = 'kpi_cell2', kpi_c2