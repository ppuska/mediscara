"""Module for the ROS Node in Robotic Cell 2"""
import argparse
import os
from typing import Optional, Tuple


import rclpy
from interfaces.msg import Robot2Control, Robot2Status

from fiware.production import Production
from fiware.model import CollaborativeOrder

from mediscara.config_ros import MessageList, NodeList
from mediscara.scripts.ros_node import ROSNode
from mediscara.scripts.socket_manager import SocketManager
from mediscara.scripts.utils import ErrorClass


class Robot2Node(ROSNode):  # pylint: disable=too-many-instance-attributes
    """Class for robotic cell no 2

    This cell contains the Kawasaki DuAro2 and the Laser Marker
    """

    INVALID_ROBOT_JOB_ERROR = ErrorClass(error_msg="The robot job was invalid", error_code=0)  # todo configure this
    ROBOT_JOB_FAILED_ERROR = ErrorClass(error_msg="The robot job has failed", error_code=0)

    __DEFAULT_ROBOT_PORT = 65432

    def __init__(self, server_url: str, robot_port: int or None):
        super().__init__(node_name=NodeList.ROBOT2_NODE.value, depends_on=[])

        if robot_port is None:
            self.get_logger().warning(f"Robot port not specified, defaulting to {self.__DEFAULT_ROBOT_PORT}")
            robot_port = Robot2Node.__DEFAULT_ROBOT_PORT

        self.__current_order = None
        self.__job_in_progress = False
        self.__job_complete = False

        # Creating status and control channels
        # subscription
        self.robot_control_sub = self.create_subscription(
            msg_type=MessageList.ROBOT2_CONTROL.value[1],
            topic=MessageList.ROBOT2_CONTROL.value[0],
            callback=self.control_callback,
            qos_profile=10,
        )

        # publisher
        self.__robot_status_pub = self.create_publisher(
            msg_type=MessageList.ROBOT2_STATUS.value[1], topic=MessageList.ROBOT2_STATUS.value[0], qos_profile=10
        )

        # Initializing the TCP Socket client
        self.__socket_client = SocketManager(
            parent=self,
            port=robot_port,
            received_callback=self.socket_received_callback,
            connected_callback=self.socket_connected_callback,
            is_server=True,
            blocking=False,
        )
        self.__socket_client.bind_and_accept()

        # Initializing the FIWARE OCB Python API
        try:
            self.__connector = Production(server_url)

        except ConnectionError:
            self.get_logger().fatal("Could not connect to the FIWARE OCB, exiting...")
            self.destroy_node()

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

    def destroy_node(self) -> bool:
        if self.__current_order is not None:
            self.__connector.set_active(self.__current_order, False)  # set as inactive job

        if self.__socket_client.connected:  # disconnect from the socket
            self.__socket_client.close()

    # endregion

    # region CALLBACKS *************************************************************************************************

    # region TCP/IP messages

    # vision system
    START_MEASURE = "MEASURE"
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
    # status
    STATUS = "STATUS"
    TRUE = "TRUE"
    FALSE = "FALSE"

    # endregion

    def control_callback(self, msg: Robot2Control):
        """Callback method for the Robot2Control message"""
        if msg.home:
            self.__socket_client.send(self.HOME)

        elif msg.start_measuring:
            self.__socket_client.send(self.START_MEASURE)

        elif msg.pause:
            self.__socket_client.send(self.PAUSE)

    def socket_received_callback(self, success: bool, incoming: str):
        """Callback function for socket receive"""
        if not success:
            self.__socket_client.connect()

        else:

            messages = incoming.split("\n")

            for msg in messages:

                if not msg:
                    continue

                self.get_logger().info(f"Got TCP message: {msg}")
                # PROCESSING THE INCOMING MESSAGE

                if msg.startswith(self.STATUS):  # status msgs
                    # status msg syntax: STATUS:MOTOR_ON:RUNNING:WAITING:ERROR
                    tokens = msg.split(":")

                    ros_msg = Robot2Status()
                    ros_msg.power = False
                    ros_msg.running = False
                    ros_msg.waiting = False
                    ros_msg.error = False

                    ros_msg.job_success = self.__job_complete
                    self.__job_complete = False

                    if tokens[1] == self.TRUE:
                        ros_msg.power = True

                    if tokens[2] == self.TRUE:
                        ros_msg.running = True

                    if tokens[3] == self.TRUE:
                        ros_msg.waiting = True

                    if tokens[4] == self.TRUE:
                        ros_msg.error = True

                    self.__robot_status_pub.publish(ros_msg)

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

                        self.__job_complete = True

                        if self.__current_order.remaining == 0:
                            # if the remaining is zero, remove the order from the database
                            self.get_logger().info(f"Removing item with id: {self.__current_order.id}")
                            self.__connector.delete_production_order(order=self.__current_order)

                    else:
                        self.__job_in_progress = True

                    self.get_logger().info("Robot job started")

                elif msg == self.JOB_SUCCESS:  # job successfully done
                    self.get_logger().info("All of the given jobs were finished")
                    self.__job_in_progress = False
                    self.__connector.set_active(self.__current_order, False)

                    # set the remaining value
                    self.__current_order.remaining -= 1
                    # update the order in the database
                    self.__connector.update_production_order_remaining(new_order=self.__current_order)

                    self.__job_complete = True

                    if (
                        self.__current_order.remaining == 0
                    ):  # if the remaining is zero, remove the order from the database
                        self.get_logger().info(f"Removing item with id: {self.__current_order.id}")
                        self.__connector.delete_production_order(order=self.__current_order)

                elif msg == self.JOB_FAILED:  # job failed
                    self.get_logger().error("Robot job failed")
                    self.__connector.set_active(self.__current_order, False)
                    self.publish_error(self.ROBOT_JOB_FAILED_ERROR)

                else:
                    self.get_logger().warn(f"Unknown robot message: {msg}")

    def socket_connected_callback(self, _):
        """Callback function for the socket connection"""
        self.__socket_client.start_receive()

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
            self.get_logger().warn("No next production order")
            # TODO configure error codes
            self.publish_error(ErrorClass(error_code=-1, error_msg="No next production order in database"))
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


SERVER_URL = "SERVER_URL"
ROBOT_IP = "ROBOT_IP"
ROBOT_PORT = "ROBOT_PORT"


def load_arguments() -> Tuple[str, str, Optional[int]]:
    """Loads the arguments from the environment variables, or from the command line arguments

    Returns:
        Tuple: The arguments (server ip, robot ip) as a tuple
    """
    server_url = os.getenv(SERVER_URL)
    robot_port = os.getenv(ROBOT_PORT)

    # argument parser
    # the arguments that are None beccome required <=> (<argument> is None)
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--server-url", type=str, dest=SERVER_URL, required=(server_url is None), help="The url of the FIWARE OCB"
    )
    arg_parser.add_argument(
        "--robot-port", type=int, dest=ROBOT_PORT, required=False, help="The port to connect to the robot via sockets"
    )

    args = vars(arg_parser.parse_args())

    # get the command line arguments, or if they are None, load the previous value
    server_url = args.get(SERVER_URL, server_url)
    robot_port = args.get(ROBOT_PORT, robot_port)

    return server_url, robot_port


def main(args=None):
    """Main function and entry point of the Node"""
    server_ip, robot_port = load_arguments()

    rclpy.init(args=args)
    robot2_node = Robot2Node(server_ip, robot_port)
    try:
        rclpy.spin(robot2_node)
    except KeyboardInterrupt:
        robot2_node.get_logger().info("Ctrl+C, stopping")

    robot2_node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
