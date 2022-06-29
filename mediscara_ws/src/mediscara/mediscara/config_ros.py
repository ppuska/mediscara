"""This is a module for setting and storing ROS2 related configuration data"""
from enum import Enum

from interfaces.msg import KPIC1 as kpi_c1
from interfaces.msg import KPIC2 as kpi_c2
from interfaces.msg import MarkerStatus as Ms
from interfaces.msg import Robot1Control as r1c
from interfaces.msg import Robot1Status as r1s
from interfaces.msg import Robot2Control as r2c
from interfaces.msg import Robot2Status as r2s
from std_msgs.msg import Bool


class NodeList(Enum):
    """Enum class for storing the Nodes and their names in the system"""

    ROBOT1_NODE = "robot1"
    ROBOT2_NODE = "robot2"
    SENSOR_NODE = "sensor"
    MARKER_NODE = "marker"
    LASER_NODE = "laser"
    HMI_COLLAB_NODE = "hmi_collaborative"
    HMI_ROBOTIC_NODE = "hmi_robotic"
    FIWARE_NODE = "is_ros2"


class MessageList(Enum):
    """Enum class for storing message topics and their respective message types"""

    MARKER_STATUS = "marker_status", Ms
    MARKER_CONTROL = "marker_control", Bool
    ROBOT1_CONTROL = "robot1_control", r1c
    ROBOT1_STATUS = "robot1_status", r1s
    ROBOT2_STATUS = "robot2_status", r2s
    ROBOT2_CONTROL = "robot2_control", r2c
    KPIC1 = "kpi_cell1", kpi_c1
    KPIC2 = "kpi_cell2", kpi_c2
