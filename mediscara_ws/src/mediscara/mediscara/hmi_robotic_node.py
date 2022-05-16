"""Module for the HMI Robotic ROS Node"""

import imp
import logging
import sys
from typing import List

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

import rclpy
from interfaces.msg import Error, Robot1Control, Robot1Status

from mediscara.scripts.hmi import HMIApp, ROSWorker
from mediscara.scripts.ros_node import QTROSNode
from mediscara.config_ros import MessageList, NodeList

from mediscara.scripts.widgets.layout.robotic_info import Ui_RoboticInfoTab
from mediscara.scripts.widgets.layout.robotic_control import Ui_RoboticControlWidget

class HMIRoboticApp(HMIApp):
    """A PyQt5 App to display the HMI interface to the user"""
    NODE_NAME = NodeList.HMIRoboticNode.value
    DEPENDS = [NodeList.Robot1Node.value]

    KPI_UPDATE_INTERVAL = 1000  # ms

    # region INNER CLASSES

    class InfoWidget(QWidget, Ui_RoboticInfoTab):
        """Class for displaying the info Widget on the info tab"""

        __POWER_ON_TEXT = "Power ON"
        __POWER_OFF_TEXT = "Power"

        __BG_COLOR_GREEN = "background-color: green;"
        __BG_COLOR_YELLOW = "background-color: yellow;"
        __BG_COLOR_BEIGE = "background-color: #f6ffc9"
        __BG_COLOR_RED = "background-color: red"

        def __init__(self, parent=None):
            super(HMIRoboticApp.InfoWidget, self).__init__(parent)
            self.setupUi(self)

            self.label_availability.setText("0 %")
            self.label_performance.setText("0 %")
            self.label_quality.setText("0 %")

        def set_error(self, error: bool):
            """Sets the error status display in the widget

            Args:
                error (bool): On or Off
            """
            if error:
                self.label_error.setStyleSheet(self.__BG_COLOR_RED)

            else:
                self.label_error.setStyleSheet("")

        def set_power(self, value: bool):
            """Sets the power value of the selected widget

            Args:
                value (bool): On or OFF
            """

            if value is True:
                self.label_power.setText(self.__POWER_ON_TEXT)
                self.label_power.setStyleSheet(self.__BG_COLOR_GREEN)

            else:
                self.label_power.setText(self.__POWER_OFF_TEXT)
                self.label_power.setStyleSheet("")

        def set_running(self, value: bool):
            """Sets the running value of the selected widget

            Args:
                value (bool): On or OFF
            """

            if value:
                self.label_running.setStyleSheet(self.__BG_COLOR_YELLOW)

            else:
                self.label_running.setStyleSheet("")

        def set_waiting(self, value: bool):
            """Sets the waiting value of the selected widget

            Args:
                value (bool): On or OFF
            """

            if value:
                self.label_waiting.setStyleSheet(self.__BG_COLOR_BEIGE)

            else:
                self.label_waiting.setStyleSheet("")

    class ControlWidget(QWidget, Ui_RoboticControlWidget):
        """Class for displaying and interfacing with the Control Widget on the control Tab"""

        def __init__(self, parent: None):
            super(HMIRoboticApp.ControlWidget, self).__init__(parent)
            self.setupUi(self)  # show ui

        @property
        def buttons(self) -> List[QPushButton]:
            """Returns all the buttons in this ui element"""
            return [
                self.button_start_session,
                self.button_end_session,
                self.button_pause,
                self.button_home,
                self.button_start_cutting
            ]

    # endregion

    def __init__(self):
        super(HMIRoboticApp, self).__init__(name=self.NODE_NAME,
                                            depends_list=self.DEPENDS,
                                            node_class=ROSNodeRobotic
                                            )

        # add info widget
        self.info_widget = HMIRoboticApp.InfoWidget(self.tab_info)
        self.info_widget_layout.addWidget(self.info_widget)

        # add control widget
        self.control_widget = HMIRoboticApp.ControlWidget(self.tab_control)
        self.control_widget_layout.addWidget(self.control_widget)

        self.showFullScreen()

        # connect button click callbacks
        for button in self.control_widget.buttons:
            button.clicked.connect(self.button_clicked_callback)

        # connect ROS signals
        self.ros_worker.signals.status.connect(self.ros_status_callback)

    # region callbacks

    def button_clicked_callback(self):
        """Callback function that gets triggered whenever a button is clicked"""

        button = self.sender()

        if button == self.control_widget.button_start_session:
            print("Start session clicked")

        elif button == self.control_widget.button_end_session:
            pass

        elif button == self.control_widget.button_pause:
            pass

        elif button == self.control_widget.button_home:
            pass

        elif button == self.control_widget.button_start_cutting:
            pass

    # endregion

    # region ROS callbacks

    def ros_status_callback(self, msg):
        """Callback method for the Robot1Status topic messages"""
        if isinstance(msg, Robot1Status):
            self.info_widget

    # endregion


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
