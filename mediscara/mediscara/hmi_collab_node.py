import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

import rclpy
from interfaces.msg import Error, Robot2Status, Robot2Control, VisionControl, KPIC2
from mediscara.scripts.hmi import HMIApp, ROSWorker, LoginStatus
from mediscara.scripts.ros_node import QTROSNode
from mediscara.config import NodeList, MessageList
from mediscara.scripts.widgets.layout.collab_info_ui import Ui_CollabInfoTab
from mediscara.scripts.widgets.layout.collab_control_ui import Ui_CollabControlWidget


class HMICollabApp(HMIApp):
    NODE_NAME = NodeList.HMINode.value
    DEPENDS = [NodeList.Robot2Node.value, NodeList.MarkerNode.value]

    __NO_LOGIN = "--nologin"

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

        def display_kpi(self, kpi: KPIC2):
            self.label_availability_rob.setText(str(kpi.availability) + '%')
            self.label_quality_rob.setText(str(kpi.quality) + '%')
            self.label_performance_rob.setText(str(kpi.performance)+ '%')

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

        @property
        def buttons(self):
            """Returns the buttons in the layout"""
            return [self.button_home_robotic,
                    self.button_home_vision,
                    self.button_start_marking,
                    self.button_measure_label,
                    self.button_measure_pcb
                    ]

    # endregion

    def __init__(self):
        super(HMICollabApp, self).__init__(name=self.NODE_NAME, depends_list=self.DEPENDS, node_class=ROSNodeCollab)

        # add info widget
        self.info_widget = HMICollabApp.InfoWidget(self.tab_info)
        self.info_widget_layout.addWidget(self.info_widget)

        # add control widget
        self.control_widget = HMICollabApp.ControlWidget(self.tab_control)
        self.control_widget_layout.addWidget(self.control_widget)

        # connect button clicks to callbacks
        for button in self.control_widget.buttons:
            assert isinstance(button, QPushButton)
            button.clicked.connect(self.button_clicked_callback)

        # connect slots and signals
        self.ros_worker.signals.kpi.connect(self.kpi_callback)
        self.ros_worker.signals.status.connect(self.status_callback)

        # command line arguments
        if sys.argv is not None:
            if self.__NO_LOGIN in sys.argv:
                # no login mode
                self.user_level = LoginStatus.ADMIN

    # region OVERRIDES *************************************************************************************************

    def ros_error_callback(self, node_name: str, msg: str, err_code: int):
        super(HMICollabApp, self).ros_error_callback(node_name, msg, err_code)

        # todo differentiate between vision system and robot
        self.info_widget.set_error(HMICollabApp.InfoWidget.VISION, True)

    def clear_errors_callback(self):
        super(HMICollabApp, self).clear_errors_callback()

        self.info_widget.set_error(HMICollabApp.InfoWidget.VISION, False)

    # endregion

    # region CALLBACKS *************************************************************************************************

    def button_clicked_callback(self):
        button_clicked = self.sender()

        # vision
        msg = VisionControl()
        if button_clicked == self.control_widget.button_home_vision:
            msg.home = True
            msg.measure_pcb = False
            msg.measure_label = False

            self.ros_worker.send_control(cell=ROSNodeCollab.VISION, msg=msg)

        elif button_clicked == self.control_widget.button_measure_pcb:
            msg.home = False
            msg.measure_pcb = True
            msg.measure_label = False

            self.ros_worker.send_control(cell=ROSNodeCollab.VISION, msg=msg)

        elif button_clicked == self.control_widget.button_measure_label:
            msg.home = False
            msg.measure_pcb = False
            msg.measure_label = True

            self.ros_worker.send_control(cell=ROSNodeCollab.VISION, msg=msg)

        # robot
        msg = Robot2Control()
        if button_clicked == self.control_widget.button_home_robotic:
            msg.home = True
            msg.start_marking = False

            self.ros_worker.send_control(cell=ROSNodeCollab.ROBOTIC, msg=msg)

        elif button_clicked == self.control_widget.button_start_marking:
            msg.home = False
            msg.start_marking = True

            self.ros_worker.send_control(cell=ROSNodeCollab.ROBOTIC, msg=msg)

    # endregion

    # region ROS CALLBACKS *********************************************************************************************

    def kpi_callback(self, msg: KPIC2):
        assert isinstance(msg, KPIC2)
        self.info_widget.display_kpi(msg)

    def status_callback(self, msg):
        if isinstance(msg, Robot2Status):
            self.info_widget.set_error(HMICollabApp.InfoWidget.ROBOTIC, msg.error)
            self.info_widget.set_power(HMICollabApp.InfoWidget.ROBOTIC, msg.power)
            self.info_widget.set_waiting(HMICollabApp.InfoWidget.ROBOTIC, msg.waiting)
            self.info_widget.set_running(HMICollabApp.InfoWidget.ROBOTIC, msg.running)

    # endregion


class ROSNodeCollab(QTROSNode):
    VISION = 0
    ROBOTIC = 1

    def __init__(self, node_name, depends_on, signals: ROSWorker.Signals):
        super(ROSNodeCollab, self).__init__(node_name=node_name, depends_on=depends_on, signals=signals)

        # publishers
        self.__robot_control = self.create_publisher(msg_type=MessageList.Robot2Control.value[1],
                                                     topic=MessageList.Robot2Control.value[0],
                                                     qos_profile=10
                                                     )

        self.__vision_control = self.create_publisher(msg_type=MessageList.VisionControl.value[1],
                                                      topic=MessageList.VisionControl.value[0],
                                                      qos_profile=10
                                                      )

        # subscriptions
        self.__kpi_subscription = self.create_subscription(msg_type=MessageList.KPIC2.value[1],
                                                           topic=MessageList.KPIC2.value[0],
                                                           callback=self.kpi_callback,
                                                           qos_profile=10
                                                           )

        self.__robot_status_subscription = self.create_subscription(
            msg_type=MessageList.Robot2Status.value[1],
            topic=MessageList.Robot2Status.value[0],
            callback=self.robot_status_callback,
            qos_profile=10
        )

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

    def send_control(self, cell: int, msg: Robot2Control or VisionControl):
        self.get_logger().debug(f"Sending command: {msg}")
        if cell == self.VISION:
            assert isinstance(msg, VisionControl)
            self.__vision_control.publish(msg)

        elif cell == self.ROBOTIC:
            assert isinstance(msg, Robot2Control)
            self.__robot_control.publish(msg)

        else:
            raise ValueError(f"Invalid cell (number: {cell})")

    def kpi_callback(self, msg: KPIC2):
        self.signals.kpi.emit(msg)

    def robot_status_callback(self, msg: Robot2Status):
        self.signals.status.emit(msg)


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
