"""Module for the ROS Node in Robotic Cell 2"""
import enum

import rclpy
from interfaces.msg import Error, MarkerStatus, Robot2Control
from mediscara.config import IPList, PortList, SQLTableNames
from mediscara.config_ros import MessageList, NodeList
from mediscara.scripts.ros_node import ROSNode
from mediscara.scripts.socket_manager import SocketManager
from mediscara.scripts.sql import Cell2Data, SQLManager
from mediscara.scripts.utils import ErrorClass
from std_msgs.msg import Bool


class Robot2Node(ROSNode):
    """Class for robotic cell no 2

    This cell contains the Kawasaki DuAro2 and the Laser Marker
    """

    SQL_TABLE_NAME = SQLTableNames.CELL2.value  # type: str
    SQL_REFRESH_INTERVAL = 5  # s

    INVALID_ROBOT_JOB_ERROR = ErrorClass(error_msg="The robot job was invalid", error_code=0)  # todo configure this
    ROBOT_JOB_FAILED_ERROR = ErrorClass(error_msg="The robot job has failed", error_code=0)

    class MarkerState(enum.Enum):  # todo remove this from code
        """Enum class for a state machine storing the Marker's state"""

        WAITING = enum.auto()
        MARKING = enum.auto()

    def __init__(self):
        super(Robot2Node, self).__init__(node_name=NodeList.Robot2Node.value, depends_on=[NodeList.MarkerNode.value])

        self.__marker_state = Robot2Node.MarkerState.WAITING
        self.__current_item = None

        # Creating status and control channels
        # subscription
        self.__marker_status_sub = self.create_subscription(
            msg_type=MessageList.MarkerStatus.value[1],
            topic=MessageList.MarkerStatus.value[0],
            callback=self.status_callback,
            qos_profile=10,
        )

        self.robot_control_sub = self.create_subscription(
            msg_type=MessageList.Robot2Control.value[1],
            topic=MessageList.Robot2Control.value[0],
            callback=self.control_callback,
            qos_profile=10,
        )

        # publisher
        self.__marker_control_pub = self.create_publisher(
            msg_type=MessageList.MarkerControl.value[1], topic=MessageList.MarkerControl.value[0], qos_profile=10
        )

        # Initializing the TCP Socket server
        self.__socket_client = SocketManager(
            parent=self,
            host=IPList.ROBOT2.value,
            port=PortList.ROBOT2.value,
            received_callback=self.socket_received_callback,
            connected_callback=self.socket_connected_callback,
            is_server=False,
            blocking=False,
        )
        self.__socket_client.connect()

        # Initializing MySQL database client
        self.__db_handler = SQLManager(table=[(self.SQL_TABLE_NAME, Cell2Data)])
        self.__sql_timer = None

        success, msg = self.__db_handler.connect_to_database()
        if not success:
            self.__sql_timer = self.create_timer(
                timer_period_sec=self.SQL_REFRESH_INTERVAL, callback=self.sql_timer_callback
            )
            self.get_logger().warn(msg)
        else:
            self.get_logger().info(msg)

        self.get_logger().info(f"{self.__class__.__name__} is online")

    # region OVERRIDES *************************************************************************************************

    def dependency_online(self, name: str, online: bool):
        if online:
            self.get_logger().info(f"Node is now online: {name}")

        else:
            self.get_logger().info("Node went offline:" + name)

    def all_depends_online(self):
        self.get_logger().info("Missing dependencies have come online")

    def depends_offline(self):
        self.get_logger().warn(f"A dependency has gone offline:\n{self.missing_dependencies}")

    def error_callback(self, msg: Error):
        if msg.node_name == NodeList.MarkerNode.value:
            # marker error
            if self.__marker_state == Robot2Node.MarkerState.MARKING:
                self.get_logger().error(f"Error while marking: [{msg.error_code}]\n\t{msg.error_msg}")
                self.__socket_client.send(self.MARKING_ERROR)

            if self.__marker_state == Robot2Node.MarkerState.WAITING:
                self.get_logger().warn(f"Marker error: [{msg.error_code}]\n\t{msg.error_msg}")

    def destroy_node(self) -> bool:
        if self.__db_handler.connected:
            self.set_in_production(False)
        self.__db_handler.close()
        return super().destroy_node()

    # endregion

    # region CALLBACKS *************************************************************************************************

    # region TCP/IP messages

    # marker
    START_MARKING = "START_MARKING"
    STOP_MARKING = "STOP_MARKING"
    MARKING_SUCCESS = "MARKING_SUCCESS"
    MARKING_ERROR = "MARKING_ERROR"
    # jobs
    JOB_INVALID = "JOB_INVALID"
    JOB_STARTED = "JOB_STARTED"
    JOB_SUCCESS = "JOB_SUCCESS"
    JOB_FAILED = "JOB_FAILED"
    JOB_REQUEST = "JOB_REQUEST"
    # homing
    HOME = "HOME"
    # pausing
    PAUSE = "PAUSE"

    # endregion

    def control_callback(self, msg: Robot2Control):
        """Callback method for the Robot2Control message"""
        if msg.home:
            self.__socket_client.send(self.HOME)

        elif msg.start_marking:
            self.__socket_client.send(self.START_MARKING)
            self.send_job()

        elif msg.pause:
            self.__socket_client.send(self.PAUSE)

        # if msg.data:
        #     self.send_job()
        #     assert isinstance(self.__current_item, Cell2Data)
        #     self.__current_item.in_production = True
        #
        #     print(self.__db_handler.update_element(table_name=self.SQL_TABLE_NAME,
        #                                            new_value=self.__current_item
        #                                            )
        #           )

    def status_callback(self, msg: MarkerStatus):
        """Callback method for the MarkerStatus messages"""
        if msg.marking_successful:
            self.get_logger().info("Marking successful")
            self.__socket_client.send(self.MARKING_SUCCESS)

    def socket_received_callback(self, success: bool, msg: str):
        """Callback function for socket receive"""
        if not success:
            self.__socket_client.connect()

        else:
            # PROCESSING THE INCOMING MESSAGE
            if msg.startswith("J|"):  # joint values
                joints = msg[2:].split("|")
                self.get_logger().debug(f"Joint values: {joints}")

            elif msg == self.JOB_REQUEST:  # handle job request
                self.send_job()

            elif msg == self.JOB_INVALID:  # job request was invalid
                self.get_logger().error("Invalid robot job")
                self.set_in_production(False)
                self.publish_error(self.INVALID_ROBOT_JOB_ERROR)

            elif msg == self.JOB_STARTED:  # job has started
                self.get_logger().info("Robot job started")
                self.set_in_production(True)

            elif msg == self.JOB_SUCCESS:  # job successfully done
                self.get_logger().info("Robot job successfully done")
                self.set_in_production(False)
                self.decrement_remaining_count()
                if self.__current_item.remaining == 0:
                    self.get_logger().info(f"Removing item with id: {self.__current_item.id}")
                    self.remove_done_item()

            elif msg == self.JOB_FAILED:  # job failed
                self.get_logger().error("Robot job failed")
                self.set_in_production(False)
                self.publish_error(self.ROBOT_JOB_FAILED_ERROR)

            elif msg == self.START_MARKING:
                self.get_logger().info("Sending marker start...")
                self.start_marking()

            elif msg == self.STOP_MARKING:
                self.get_logger().info("Sending marker stop...")
                self.stop_marking()

            else:
                self.get_logger().warn(f"Unknown robot message: {msg}")

    def socket_connected_callback(self, _):
        """Callback function for the socket connection"""
        self.__socket_client.start_receive()

    def sql_timer_callback(self):
        """Callback method for a timer to check the MySQL database connection"""
        if not self.__db_handler.connected:
            success, msg = self.__db_handler.connect_to_database()
            if success:
                self.get_logger().info(msg)

            else:
                self.get_logger().warn(msg)

    # endregion

    # region MESSAGE GENERATION ****************************************************************************************

    def start_marking(self):
        """Send a MarkerControl ROS message to start the marking"""
        msg = Bool()
        msg.data = True

        self.__marker_control_pub.publish(msg)
        self.__marker_state = self.MarkerState.MARKING

    def stop_marking(self):
        """Sends a MarkerControl ROS message to stop the marking"""
        msg = Bool()
        msg.data = False

        self.__marker_control_pub.publish(msg)
        self.__marker_state = self.MarkerState.WAITING

    # endregion

    # region METHODS ***************************************************************************************************

    def get_current_item(self):
        """Sets the current item variable"""
        self.__current_item = self.__db_handler.get_next_element(self.SQL_TABLE_NAME)  # type: Cell2Data

    def send_job(self):
        """Searches for the next item in the MySQL database and sends it to the robot as a job request"""
        self.__current_item = self.__db_handler.get_next_element(self.SQL_TABLE_NAME)  # type: Cell2Data

        if self.__current_item is None:
            self.get_logger().warn("No next item in database")
            return

        job_string = (
            f"JS:{self.__current_item.inc_type.upper()}_"
            f"{self.__current_item.part_type.upper()}:"
            f"{self.__current_item.remaining}"
        )

        self.get_logger().info(f"Sending job select command: {job_string}")
        self.__socket_client.send(job_string)  # todo update database

    def decrement_remaining_count(self):
        """Decrements the current item's 'remaining' count by one"""
        if self.__current_item is None:
            self.get_logger().warn("No item loaded from database, loading now...")
            self.get_current_item()

        assert isinstance(self.__current_item, Cell2Data)
        self.__current_item.remaining -= 1

        success = self.__db_handler.update_element(table_name=self.SQL_TABLE_NAME, new_value=self.__current_item)

        return success

    def remove_done_item(self):
        """Removes the current item if its 'remaining' counter is zero"""
        self.get_current_item()

        assert isinstance(self.__current_item, Cell2Data)

        if self.__current_item.remaining > 0:
            self.get_logger().warn("Cannot remove an item which has remaining jobs")
            return

        success = self.__db_handler.delete_element(id_=self.__current_item.id, table_name=self.SQL_TABLE_NAME)

        return success

    def set_in_production(self, in_production: bool) -> bool:
        """Sets the current item's 'in_production' value to the given value"""
        if self.__current_item is None:
            self.get_logger().warn("No item loaded from database, loading now...")
            self.get_current_item()

        assert isinstance(self.__current_item, Cell2Data)
        self.__current_item.in_production = in_production

        success = self.__db_handler.update_element(table_name=self.SQL_TABLE_NAME, new_value=self.__current_item)

        return success

    # endregion


def main(args=None):
    """Main function and entry point of the Node"""
    rclpy.init(args=args)

    robot2_node = Robot2Node()
    try:
        rclpy.spin(robot2_node)
    except KeyboardInterrupt:
        robot2_node.get_logger().info("Ctrl+C, stopping")

    robot2_node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
