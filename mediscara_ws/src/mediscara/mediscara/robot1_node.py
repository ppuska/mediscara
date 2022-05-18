"""Module for the Robot 1 cell"""
import rclpy
from interfaces.msg import Error
from mediscara.config_ros import NodeList
from mediscara.scripts.ros_node import ROSNode


class Robot1Node(ROSNode):
    """Class for robotic cell no 1

    This cell contains the Kawasaki RS050N and the Laser Cutter
    """

    def __init__(self):
        super().__init__(node_name=NodeList.Robot1Node.value, depends_on=[NodeList.LaserNode.value])

        self.get_logger().info(f"{self.__class__.__name__} is online")

    def error_callback(self, msg: Error):
        self.get_logger().error(f"ERROR: {msg.node_name}\t{msg.error_msg}\t{msg.error_code}")  # TODO implement this

    def dependency_online(self, name: str, online: bool):
        pass

    def dependency_offline(self):
        pass


def main(args=None):
    """Entry point for the ROS Node

    Args:
        args (List[str], optional): arguments for the rclpy runtime. Defaults to None.
    """
    rclpy.init(args=args)

    robot1_node = Robot1Node()
    try:
        rclpy.spin(robot1_node)
    except KeyboardInterrupt:
        robot1_node.get_logger().info("Ctrl+C, stopping")

    robot1_node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
