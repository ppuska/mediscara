"""Module for the HMI Robotic ROS Node"""

import logging
import sys
from typing import List

from PyQt5.QtWidgets import QApplication, QWidget

import rclpy
from interfaces.msg import Error, Robot1Control

from mediscara.scripts.hmi import HMIApp, ROSWorker
from mediscara.scripts.ros_node import QTROSNode
from mediscara.config_ros import MessageList, NodeList

from mediscara.scripts.widgets.layout.robotic_info import Ui_RoboticInfoTab

class HMIRoboticApp(HMIApp):
    """A PyQt5 App to display the HMI interface to the user"""
    NODE_NAME = NodeList.HMIRoboticNode.value
    DEPENDS = [NodeList.Robot1Node.value]

    KPI_UPDATE_INTERVAL = 1000  # ms

    # region INNER CLASSES

    class InfoWidget(QWidget, Ui_RoboticInfoTab):
        """Class for displaying the info Widget on the info tab"""

        def __init__(self, parent=None):
            super(HMIRoboticApp.InfoWidget, self).__init__(parent)
            self.setupUi(self)

            self.label_availability.setText("0 %")
            self.label_performance.setText("0 %")
            self.label_quality.setText("0 %")

    # endregion

    def __init__(self):
        super(HMIRoboticApp, self).__init__(name=self.NODE_NAME,
                                            depends_list=self.DEPENDS,
                                            node_class=ROSNodeRobotic
                                            )

        # add info widget
        self.info_widget = HMIRoboticApp.InfoWidget(self.tab_info)
        self.info_widget_layout.addWidget(self.info_widget)

        self.showFullScreen()


class ROSNodeRobotic(QTROSNode):
    """Class for the Robotic ROS Node in the HMI Application"""

    def __init__(self, node_name: str, depends_on: List[str], signals: ROSWorker.Signals):
        super(ROSNodeRobotic, self).__init__(node_name=node_name, depends_on=depends_on, signals=signals)

        # publishers
        self.__control = self.create_publisher(msg_type=MessageList.Robot1Control.value[1],
                                               topic=MessageList.Robot1Control.value[0],
                                               qos_profile=10
                                               )

        self.__kpi = self.create_publisher(msg_type=MessageList.KPIC1.value[1],
                                           topic=MessageList.KPIC1.value[0],
                                           qos_profile=10
                                           )


    def error_callback(self, msg: Error):
        self.signals.new_error.emit(msg.node_name, msg.errir_msg, msg.error_code)

    def all_depends_online(self):
        self.get_logger().info("All dependencies are online")

    def dependency_online(self, name: str, online: bool):
        if online:
            self.get_logger().info(f"A dependency has come online: {name}")

        else:
            self.get_logger().info(f"A dependency has gone offline: {name}")

        self.signals.dependency_online.emit(name, online)

    def depends_offline(self):
        self.signals.dependency_online.emit("", False)
        self.signals.new_error.emit("Internal error", "A dependency node has gone offline", 0)

    def load_nodes(self):
        self.get_logger().debug("Loading nodes")
        all_nodes = self.dependencies
        missing_nodes = self.missing_dependencies
        self.signals.nodes_loaded.emit(all_nodes, missing_nodes)

    def send_control(self, _: int, msg: object):
        self.get_logger().debug(f"Sending command: {msg}")

        assert isinstance(msg, Robot1Control)
        self.__control.publish(msg)

    def send_kpi(self, msg):
        self.__kpi.publish(msg)


def main(args=None):
    """Entry point for the ROS launch"""
    rclpy.init(args=args)
    try:
        app = QApplication(sys.argv)
        ui_window = HMIRoboticApp()
        ui_window.show()
        sys.exit(app.exec())

    except KeyboardInterrupt:
        print("\nStopping")


if __name__ == '__main__':
    main()
