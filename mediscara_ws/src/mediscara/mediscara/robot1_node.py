"""Module for the Robot 1 cell"""
import argparse
import os
from typing import Optional, Tuple

from mediscara.scripts.socket_manager import SocketManager
import rclpy
from interfaces.msg import Error, Robot1Control
from mediscara.config_ros import MessageList, NodeList
from mediscara.scripts.ros_node import ROSNode

from fiware.production import Production

class Robot1Node(ROSNode):
    """Class for robotic cell no 1

    This cell contains the Kawasaki RS050N and the Laser Cutter
    """

    __DEFAULT_ROBOT_PORT = 65432

    def __init__(self, server_url: str, robot_ip: str, robot_port: int):
        super().__init__(node_name=NodeList.ROBOT1_NODE.value, depends_on=[NodeList.LASER_NODE.value])

        if robot_port is None:
            robot_port = Robot1Node.__DEFAULT_ROBOT_PORT

        self.__current_order = None

        # subscriptions
        self.create_subscription(
            msg_type=MessageList.ROBOT1_CONTROL.value[1],
            topic=MessageList.ROBOT1_CONTROL.value[0],
            callback=self.status_callback,
            qos_profile=10
        )

        # TODO make laser control publisher

        # Initialize the FIWARE OCB Python API
        try:
            self.__connector = Production(server_url)

        except ConnectionError:
            self.get_logger().fatal("Could not connect to the FIWARE OCB, exiting...")
            self.destroy_node()
            return

        self.__socket_client = SocketManager(
            parent=self,
            host=robot_ip,
            port=robot_port,
            received_callback=self.socket_received_callback,
            connected_callback=self.socket_connected_callback,
            is_server=False,
            blocking=False
        )

        self.__socket_client.connect()

        self.get_logger().info(f"{self.__class__.__name__} is online")

    # region TCP/IP messages

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


    # region CALLBACKS

    def control_callback(self, msg: Robot1Control):
        raise NotImplementedError

    def socket_received_callback(self, success: bool, msg: str):
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

            else:
                self.get_logger().warn(f"Unknown robot message: {msg}")

    def socket_connected_callback(self, _):
        """Callback function for the socket connection"""
        self.__socket_client.start_receive()

    # endregion

    # region OVERRIDES

    def error_callback(self, msg: Error):
        self.get_logger().error(f"ERROR: {msg.node_name}\t{msg.error_msg}\t{msg.error_code}")  # TODO implement this

    def dependency_online(self, name: str, online: bool):
        pass

    def dependency_offline(self):
        pass

    def destroy_node(self):
        if self.__current_order is not None:
            self.__connector.set_active(self.__current_order, False)  # set as inactive job

        if self.__socket_client.connected:  # disconnect from the socket
            self.__socket_client.close()

    # endregion

SERVER_URL = "SERVER_URL"
ROBOT_IP = "ROBOT_IP"
ROBOT_PORT = "ROBOT_PORT"


def load_arguments() -> Tuple[str, str, Optional[int]]:
    """Loads the arguments from the environment variables, or from the command line arguments

    Returns:
        Tuple: The arguments (server ip, robot ip, robot port) as a tuple
    """
    server_url = os.getenv(SERVER_URL)
    robot_ip = os.getenv(ROBOT_IP)
    robot_port = os.getenv(ROBOT_PORT)

    # argument parser
    # the arguments that are None beccome required <=> (<argument> is None)
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--server-url',
                            type=str,
                            dest=SERVER_URL,
                            required=(server_url is None),
                            help="The url of the FIWARE OCB"
                            )
    arg_parser.add_argument('--robot-ip',
                            type=str,
                            dest=ROBOT_IP,
                            required=(robot_ip is None),
                            help="The IP address of the robot"
                            )
    arg_parser.add_argument("--robot-port",
                            type=int,
                            dest=ROBOT_PORT,
                            required=False,
                            help="The port to connect to the robot via sockets"
                            )

    args = vars(arg_parser.parse_args())

    # get the command line arguments, or if they are None, load the previous value
    server_url = args.get(SERVER_URL, server_url)
    robot_ip = args.get(ROBOT_IP, robot_ip)
    robot_port = args.get(ROBOT_PORT, robot_port)

    return server_url, robot_ip, robot_port



def main(args=None):
    """Entry point for the ROS Node

    Args:
        args (List[str], optional): arguments for the rclpy runtime. Defaults to None.
    """
    server_ip, robot_ip, robot_port = load_arguments()

    rclpy.init(args=args)

    robot1_node = Robot1Node(server_ip, robot_ip, robot_port)
    try:
        rclpy.spin(robot1_node)
    except KeyboardInterrupt:
        robot1_node.get_logger().info("Ctrl+C, stopping")

    robot1_node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
