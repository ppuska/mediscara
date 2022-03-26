import sys

from PyQt5.QtWidgets import QApplication

import rclpy
from interfaces.msg import Error
from .scripts.hmi import HMIApp, ROSWorker
from .scripts.ros_node import QTROSNode
from .scripts.utils import NodeList


class HMICollabApp(HMIApp):
    NODE_NAME = NodeList.HMINode.value
    DEPENDS = [NodeList.Robot2Node.value, NodeList.MarkerNode.value]

    def __init__(self):
        super(HMICollabApp, self).__init__(name=self.NODE_NAME, depends_list=self.DEPENDS, node_class=ROSNodeCollab)


class ROSNodeCollab(QTROSNode):

    def __init__(self, node_name, depends_on, signals: ROSWorker.Signals):
        super(ROSNodeCollab, self).__init__(node_name=node_name, depends_on=depends_on, signals=signals)

        self.get_logger().info("ROS node online")

    def error_callback(self, msg: Error):
        self.signals.new_error.emit(msg.node_name, msg.error_msg, msg.error_code)

    def depends_online(self):
        pass

    def depends_offline(self):
        pass

    def load_info(self):
        pass

    def load_nodes(self):
        self.get_logger().info("Loading nodes")
        all_nodes = self.dependencies
        missing_nodes = self.missing_dependencies
        self.signals.nodes_loaded.emit(all_nodes, missing_nodes)

    def send_control(self):
        pass


class SQLManager:
    pass


def main(args=None):
    rclpy.init(args=args)
    try:
        app = QApplication(sys.argv)
        ui_window = HMICollabApp()
        ui_window.show()
        sys.exit(app.exec())
    except KeyboardInterrupt:
        print("Stopping")


if __name__ == '__main__':
    main()
