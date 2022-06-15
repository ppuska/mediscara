"""Module for the ROS Node in Robotic Cell 2"""
import enum

import rclpy
from interfaces.msg import Error, MarkerStatus, Robot2Control
from std_msgs.msg import Bool
from mediscara.config import IPList, PortList
from mediscara.config_ros import MessageList, NodeList
from mediscara.scripts.ros_node import ROSNode
from mediscara.scripts.socket_manager import SocketManager
from mediscara.scripts.utils import ErrorClass
from fiware.production import Production
from fiware.model import CollaborativeOrder


class Robot2Node(ROSNode):
    """Class for robotic cell no 2

    This cell contains the Kawasaki DuAro2 and the Laser Marker
    """

    SERVER_URL = 'http://localhost:1026'

    INVALID_ROBOT_JOB_ERROR = ErrorClass(error_msg="The robot job was invalid", error_code=0)  # todo configure this
    ROBOT_JOB_FAILED_ERROR = ErrorClass(error_msg="The robot job has failed", error_code=0)

    class MarkerState(enum.Enum):  # todo remove this from code
        """Enum class for a state machine storing the Marker's state"""

        WAITING = enum.auto()
        MARKING = enum.auto()

    def __init__(self):
        super().__init__(node_name=NodeList.ROBOT2_NODE.value, depends_on=[NodeList.MARKER_NODE.value])

        self.__marker_state = Robot2Node.MarkerState.WAITING
        self.__current_order = None
        self.__job_in_progress = False

        # Creating status and control channels
        # subscription
        self.create_subscription(
            msg_type=MessageList.MARKER_STATUS.value[1],
            topic=MessageList.MARKER_STATUS.value[0],
            callback=self.status_callback,
            qos_profile=10,
        )

        self.robot_control_sub = self.create_subscription(
            msg_type=MessageList.ROBOT2_CONTROL.value[1],
            topic=MessageList.ROBOT2_CONTROL.value[0],
            callback=self.control_callback,
            qos_profile=10,
        )

        # publisher
        self.__marker_control_pub = self.create_publisher(
            msg_type=MessageList.MARKER_CONTROL.value[1],
            topic=MessageList.MARKER_CONTROL.value[0],
            qos_profile=10
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

        # Initializing the FIWARE OCB Python API
        self.__connector = Production(Robot2Node.SERVER_URL)

        self.get_logger().info(f"{self.__class__.__name__} is online")

    # region OVERRIDES *************************************************************************************************

    def dependency_online(self, name: str, online: bool):
        if online:
            self.get_logger().info(f"Node is now online: {name}")

        else:
            self.get_logger().info("Node went offline:" + name)

    def all_depends_online(self):
        self.get_logger().info("Missing dependencies have come online")

    def dependency_offline(self):
        self.get_logger().warn(f"A dependency has gone offline:\n{self.missing_dependencies}")

    def error_callback(self, msg: Error):
        if msg.node_name == NodeList.MARKER_NODE.value:
            # marker error
            if self.__marker_state == Robot2Node.MarkerState.MARKING:
                self.get_logger().error(f"Error while marking: [{msg.error_code}]\n\t{msg.error_msg}")
                self.__socket_client.send(self.MARKING_ERROR)

            if self.__marker_state == Robot2Node.MarkerState.WAITING:
                self.get_logger().warn(f"Marker error: [{msg.error_code}]\n\t{msg.error_msg}")

    def destroy_node(self) -> bool:
        if self.__current_order is not None:
            self.__connector.set_active(self.__current_order, False)  # set as inactive job

        if self.__socket_client.connected:  # disconnect from the socket
            self.__socket_client.close()

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
        self.get_logger().info("Control callback")
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
                self.__connector.set_active(self.__current_order, False)
                self.publish_error(self.INVALID_ROBOT_JOB_ERROR)

            elif msg == self.JOB_STARTED:  # job has started
                if self.__job_in_progress:
                    # a job was in progress
                    self.get_logger().info("Job successfully done")

                    # set the remaining value
                    self.__current_order.remaining -= 1
                    # update the order in the database
                    self.__connector.update_production_order_remaining(new_order=self.__current_order)

                    if self.__current_order.remaining == 0:
                        # if the remaining is zero, remove the order from the database
                        self.get_logger().info(f"Removing item with id: {self.__current_order.id}")
                        self.__connector.delete_production_order(order=self.__current_order)

                else:
                    self.__job_in_progress = True

                self.get_logger().info("Robot job started")

            elif msg == self.JOB_SUCCESS:  # job successfully done
                self.get_logger().info("Robot job successfully done")
                self.__job_in_progress = False
                self.__connector.set_active(self.__current_order, False)

                # set the remaining value
                self.__current_order.remaining -= 1
                # update the order in the database
                self.__connector.update_production_order_remaining(new_order=self.__current_order)

                if self.__current_order.remaining == 0:  # if the remaining is zero, remove the order from the database
                    self.get_logger().info(f"Removing item with id: {self.__current_order.id}")
                    self.__connector.delete_production_order(order=self.__current_order)

            elif msg == self.JOB_FAILED:  # job failed
                self.get_logger().error("Robot job failed")
                self.__connector.set_active(self.__current_order, False)
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


    def send_job(self):
        """Searches for the next item in the FIWARE OCB production orders"""

        # Communication with the robot:
        # JS:<Incubator type (upper case)>_<Part type (upper case)>:<how many to make>
        # which the robot interprets as
        # JS:<program_name>:<number of cycles>

        orders = self.__connector.load_production_orders(order=CollaborativeOrder)

        if not orders:
            self.get_logger().warn("No next production order")  # TODO add message to the HMI
            return

        self.__current_order = orders[0]

        assert isinstance(self.__current_order, CollaborativeOrder)

        job_string = (
            f"JS:{self.__current_order.incubator_type.upper()}_"
            f"{self.__current_order.part_type.upper()}:"
            f"{self.__current_order.remaining}"
        )

        self.__socket_client.send(job_string)
        self.__connector.set_active(order=self.__current_order, active=True)  # sets the order to be active

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
