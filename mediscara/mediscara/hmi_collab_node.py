import sys

from PyQt5.QtWidgets import QApplication, QWidget

import rclpy
from interfaces.msg import Error
from mediscara.scripts.hmi import HMIApp, ROSWorker
from mediscara.scripts.ros_node import QTROSNode
from mediscara.config import NodeList
from mediscara.scripts.widgets.layout.collab_info_ui import Ui_CollabInfoTab
from mediscara.scripts.widgets.layout.collab_control_ui import Ui_CollabControlWidget


class HMICollabApp(HMIApp):
    NODE_NAME = NodeList.HMINode.value
    DEPENDS = [NodeList.Robot2Node.value, NodeList.MarkerNode.value]

    # region INNER CLASSES *********************************************************************************************

    class InfoWidget(QWidget, Ui_CollabInfoTab):
        """Class for displaying the info QWidget on the info tab"""

        VISION = 0
        ROBOTIC = 1

        __POWER_ON_TEXT = "Power ON"
        __POWER_OFF_TEXT = "Power"

        __BG_COLOR_GREEN = "background-color: green;"
        __BG_COLOR_YELLOW = "background-color: yellow;"
        __BG_COLOR_BEIGE = "background-color: #f6ffc9"
        __BG_COLOR_RED = "background-color: red"

        def __init__(self, parent=None):
            super(HMICollabApp.InfoWidget, self).__init__(parent)
            self.setupUi(self)

            self.label_availability_vis.setText("0 %")
            self.label_availability_rob.setText("0 %")
            self.label_performance_vis.setText("0 %")
            self.label_performance_rob.setText("0 %")
            self.label_quality_vis.setText("0 %")
            self.label_quality_rob.setText("0 %")

        def set_power(self, box: int, value: bool):
            if box == self.VISION:
                label = self.label_power_vis

            elif box == self.ROBOTIC:
                label = self.label_power_rob

            else:
                raise ValueError("Invalid box number")

            if value is True:
                label.setText(self.__POWER_ON_TEXT)
                label.setStyleSheet(self.__BG_COLOR_GREEN)

            else:
                label.setText(self.__POWER_OFF_TEXT)
                label.setStyleSheet("")

        def set_running(self, box: int, value: bool):
            if box == self.VISION:
                label = self.label_running_vis

            elif box == self.ROBOTIC:
                label = self.label_running_rob

            else:
                raise ValueError("Invalid box number")

            if value:
                label.setStyleSheet(self.__BG_COLOR_YELLOW)

            else:
                label.setStyleSheet("")

        def set_waiting(self, box: int, value: bool):
            if box == self.VISION:
                label = self.label_waiting_vis

            elif box == self.ROBOTIC:
                label = self.label_waiting_rob

            else:
                raise ValueError("Invalid box number")

            if value:
                label.setStyleSheet(self.__BG_COLOR_BEIGE)

            else:
                label.setStyleSheet("")

        def set_error(self, box: int, value: bool):
            if box == self.VISION:
                label = self.label_error_vis

            elif box == self.ROBOTIC:
                label = self.label_error_rob

            else:
                raise ValueError("Invalid box number")

            if value:
                label.setStyleSheet(self.__BG_COLOR_RED)

            else:
                label.setStyleSheet("")

    class ControlWidget(QWidget, Ui_CollabControlWidget):

        def __init__(self, parent=None):
            super(HMICollabApp.ControlWidget, self).__init__(parent=parent)
            self.setupUi(self)

    # endregion

    def __init__(self):
        super(HMICollabApp, self).__init__(name=self.NODE_NAME, depends_list=self.DEPENDS, node_class=ROSNodeCollab)

        # add info widget
        self.info_widget = HMICollabApp.InfoWidget(self.tab_info)
        self.info_widget_layout.addWidget(self.info_widget)

        # add control widget
        self.control_widget = HMICollabApp.ControlWidget(self.tab_control)
        self.control_widget_layout.addWidget(self.control_widget)

    # region OVERRIDES *************************************************************************************************

    def ros_error_callback(self, node_name: str, msg: str, err_code: int):
        super(HMICollabApp, self).ros_error_callback(node_name, msg, err_code)

        # todo differentiate between vision system and robot
        self.info_widget.set_error(HMICollabApp.InfoWidget.VISION, True)

    def clear_errors_callback(self):
        super(HMICollabApp, self).clear_errors_callback()

        self.info_widget.set_error(HMICollabApp.InfoWidget.VISION, False)

    # endregion


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
        self.get_logger().debug("Loading nodes")
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
