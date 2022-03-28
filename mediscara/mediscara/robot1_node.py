import rclpy
from interfaces.msg import Error

from mediscara.scripts.ros_node import ROSNode
from mediscara.config import NodeList


class Robot1Node(ROSNode):
    """Class for robotic cell no 1

    This cell contains the Kawasaki RS050N and the Laser Cutter
    """

    def __init__(self):
        super(Robot1Node, self).__init__(
            node_name=NodeList.Robot1Node.value,
            depends_on=[NodeList.LaserNode.value]
        )

        self.get_logger().info(f"{self.__class__.__name__} is online")

    def error_callback(self, msg: Error):
        self.get_logger().error(f"ERROR: {msg.node_name}\t{msg.error_msg}\t{msg.error_code}")  # TODO implement this

    def depends_online(self):
        pass

    def depends_offline(self):
        pass


def main(args=None):
    rclpy.init(args=args)

    robot1_node = Robot1Node()
    try:
        rclpy.spin(robot1_node)
    except KeyboardInterrupt:
        robot1_node.get_logger().info("Ctrl+C, stopping")

    robot1_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
