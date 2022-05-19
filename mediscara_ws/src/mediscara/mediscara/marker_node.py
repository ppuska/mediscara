"""Module for the marker ROS node"""
import enum
from time import time

import rclpy
from interfaces.msg import Error, MarkerStatus

from std_msgs.msg import Bool

from mediscara.config_ros import MessageList, NodeList
from mediscara.scripts.ros_node import ROSNode
from mediscara.scripts.socket_manager import SocketManager
from mediscara.scripts.utils import ErrorClass as UtilsError


class MarkerNode(ROSNode):  # todo fix error spamming issue
    """Class for the ROS node of the laser marker"""

    # Marker status
    class MarkerStatus(enum.Enum):
        """Enum class for storing marker status values"""

        WAITING_FOR_CONNECTION = 0
        IDLE = 1
        MARKING = 2
        ERROR = 3

    # Error messages
    MARKING_START_ERROR = UtilsError(error_msg="Could not start marking", error_code=61)
    MARKER_CONNECTION_ERROR = UtilsError(error_msg="Could not connect to marker", error_code=62)
    MARKER_BUSY_ERROR = UtilsError(error_msg="Marker is busy", error_code=63)

    # Messages for the socket communication
    INFO_MESSAGE = "info"
    START_LASER_MSG = "start_laser"
    LASER_STARTED_MSG = "laser_started"
    TOP_LASER_MSG = "stop_laser"
    LASER_STOPPED_MSG = "laser_stopped"
    LASER_ERROR_MSG = "laser_error"
    LASER_BUSY_MSG = "laser_busy"
    TRUE = "true"
    FALSE = "false"

    def __init__(self):
        super(MarkerNode, self).__init__(NodeList.MARKER_NODE.value)

        self.__marker_socket = SocketManager(
            parent=self,
            host="localhost",
            port=65432,
            is_server=False,
            blocking=False,
            connected_callback=self.__socket_connected_callback,
            received_callback=self.__socket_received_callback,
        )
        self.__marker_socket.connect()
        self.__marker_on_time = 0

        """Creating subscriptions"""
        self.__marker_control_subscription = self.create_subscription(
            msg_type=MessageList.MARKER_CONTROL.value[1],  # todo implement custom message
            topic=MessageList.MARKER_CONTROL.value[0],
            callback=self.marker_control_callback,
            qos_profile=10,
        )

        """Creating publishers"""
        self.__marker_status_publisher = self.create_publisher(
            msg_type=MessageList.MARKER_STATUS.value[1], topic=MessageList.MARKER_STATUS.value[0], qos_profile=10
        )

        self.get_logger().info(f"{self.__class__.__name__} started")

    # region OVERRIDES *************************************************************************************************

    def error_callback(self, msg: Error):
        pass

    def depends_online(self):
        pass

    def depends_offline(self):
        pass

    def all_depends_online(self):
        pass

    def dependency_online(self, name: str, online: bool):
        pass

    # endregion

    # region NODE CALLBACKS ********************************************************************************************

    def marker_control_callback(self, msg: Bool):
        """Callback method for the marker control ROS message
        Args:
            msg (Bool): The incoming message
        """
        if msg.data:
            self.get_logger().info("Starting marking")
            self.__marker_socket.send(self.START_LASER_MSG)

        else:
            self.get_logger().info("Stopping marking")
            self.__marker_socket.send(self.TOP_LASER_MSG)

    # endregion

    # region SOCKET CALLBACKS ******************************************************************************************

    def __socket_connected_callback(self, _):
        self.__marker_socket.start_receive()

    def __socket_received_callback(self, success: bool, message: str):
        if not success:
            self.__marker_socket.connect()

        else:
            self.get_logger().info("Message: " + message)

            # Process the incoming message
            if message == self.LASER_STARTED_MSG:
                self.__marker_on_time = time()  # store marker on time

            elif message == self.LASER_STOPPED_MSG:
                self.__marker_on_time = time() - self.__marker_on_time  # calculate marker on time
                self.get_logger().info(f"Marking duration: {self.__marker_on_time} s")

                # create marker message
                marker_msg = MarkerStatus()
                marker_msg.marking_successful = True
                marker_msg.marking_duration = self.__marker_on_time
                self.__marker_status_publisher.publish(marker_msg)

                self.__marker_on_time = 0  # reset marker on time

            elif self.LASER_ERROR_MSG in message:
                split = message.split(":")
                error = UtilsError(error_msg=split[0], error_code=int(split[1]))

                self.publish_error(error)

            elif message == self.LASER_BUSY_MSG:
                self.get_logger().warn("Marker is busy")
                self.publish_error(self.MARKER_BUSY_ERROR)

    # endregion


def main(args=None):
    rclpy.init(args=args)

    raspi_marker_node = MarkerNode()

    try:
        rclpy.spin(raspi_marker_node)
    except KeyboardInterrupt:
        raspi_marker_node.get_logger().info("Ctrl+C detected stopping node...")

    raspi_marker_node.destroy_node()
    rclpy.shutdown()


if __name__ == "__man__":
    main()
