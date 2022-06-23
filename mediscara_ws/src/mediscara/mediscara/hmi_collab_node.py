"""Module for the HMI Collaborative App"""
import logging
import sys
from enum import Enum, auto
from telnetlib import STATUS
from typing import List

import rclpy

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget

from interfaces.msg import KPIC2, Error, Robot2Control, Robot2Status, VisionControl
from mediscara.config_ros import MessageList, NodeList
from mediscara.scripts.hmi import HMIApp, ROSWorker
from mediscara.scripts.kpi import KPI
from mediscara.scripts.ros_node import QTROSNode
from mediscara.scripts.widgets.layout.collab_control_ui import Ui_CollabControlWidget
from mediscara.scripts.widgets.layout.collab_info_ui import Ui_CollabInfoTab


class HMICollabApp(HMIApp):  # pylint: disable=too-many-instance-attributes
    """Subclass of HMIApp"""

    NODE_NAME = NodeList.HMI_COLLAB_NODE.value
    DEPENDS = [NodeList.ROBOT2_NODE.value, NodeList.MARKER_NODE.value]

    KPI_UPDATE_INTERVAL = 1000  # ms
    KPI_QUOTA = 7000

    # region INNER CLASSES *********************************************************************************************

    class STATUS(Enum):
        """Enum class to implement a state machine of the production state"""

        IDLE = auto()
        WORKING = auto()
        PAUSED = auto()

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
            super().__init__(parent)
            self.setupUi(self)

            self.label_availability_vis.setText("0 %")
            self.label_availability_rob.setText("0 %")
            self.label_performance_vis.setText("0 %")
            self.label_performance_rob.setText("0 %")
            self.label_quality_vis.setText("0 %")
            self.label_quality_rob.setText("0 %")

        def display_kpi(self, box: int, *, availability: float, quality: float, performance: float):
            """Displays the KPI data to the widget"""
            if box == self.ROBOTIC:
                self.label_availability_rob.setText(f"{availability*100:.1f}%")
                self.label_quality_rob.setText(f"{quality*100:.1f}%")
                self.label_performance_rob.setText(f"{performance*100:.1f}%")

            elif box == self.VISION:
                self.label_availability_vis.setText(f"{availability:.1f}%")
                self.label_quality_vis.setText(f"{quality:.1f}%")
                self.label_performance_vis.setText(f"{performance:.1f}%")

            else:
                raise ValueError(f"Invalid input number ({box})")

        def set_power(self, box: int, value: bool):
            """Sets the power value of the selected widget

            Args:
                box (int): Number of the cell, use InfoWidget.VISION or InfoWidget.ROBOTIC
                value (bool): On or OFF

            Raises:
                ValueError: If the box argument is invalid
            """
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
            """Sets the running value of the selected widget

            Args:
                box (int): Number of the cell, use InfoWidget.VISION or InfoWidget.ROBOTIC
                value (bool): On or OFF

            Raises:
                ValueError: If the box argument is invalid
            """
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
            """Sets the waiting value of the selected widget

            Args:
                box (int): Number of the cell, use InfoWidget.VISION or InfoWidget.ROBOTIC
                value (bool): On or OFF

            Raises:
                ValueError: If the box argument is invalid
            """
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
            """Sets the error value of the selected widget

            Args:
                box (int): Number of the cell, use InfoWidget.VISION or InfoWidget.ROBOTIC
                value (bool): On or OFF

            Raises:
                ValueError: If the box argument is invalid
            """
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
        """Class for the Control Widget in the Collaborative HMI App"""

        def __init__(self, parent=None):
            super(HMICollabApp.ControlWidget, self).__init__(parent=parent)
            self.setupUi(self)

            self.__locked_vision = False
            self.__locked_robotic = False

        def lock_control_vision(self, lock: bool):
            """Locks the controls of the vision system"""
            self.button_start_session.setEnabled(not lock)
            self.button_home.setEnabled(not lock)
            self.button_measure_label.setEnabled(not lock)
            self.button_measure_pcb.setEnabled(not lock)

            self.__locked_vision = lock

        def lock_control_robotic(self, lock: bool):
            """Locks the controls of the robotic system"""
            self.button_start_session_rob.setEnabled(not lock)
            self.button_home_rob.setEnabled(not lock)
            self.button_start_marking.setEnabled(not lock)

            self.__locked_robotic = lock

        def set_state_vision(self, state: STATUS):
            """Sets the button states according to the input state"""
            if not self.__locked_vision:  # only update it if it is not locked
                if state == HMICollabApp.STATUS.IDLE:
                    self.button_start_session.setEnabled(True)
                    self.button_pause.setEnabled(False)
                    self.button_end_session.setEnabled(False)

                    self.button_pause.setText("PAUSE")

                elif state == HMICollabApp.STATUS.PAUSED:
                    self.button_pause.setText("RESUME")

                elif state == HMICollabApp.STATUS.WORKING:
                    self.button_start_session.setEnabled(False)
                    self.button_pause.setEnabled(True)
                    self.button_end_session.setEnabled(True)

                    self.button_pause.setText("PAUSE")

        def set_state_robotic(self, state: STATUS):
            """Sets the button states according to the input state"""
            if not self.__locked_robotic:
                if state == HMICollabApp.STATUS.IDLE:
                    self.button_start_session_rob.setEnabled(True)
                    self.button_pause_rob.setEnabled(False)
                    self.button_end_session_rob.setEnabled(False)

                    self.button_pause_rob.setText("PAUSE")

                elif state == HMICollabApp.STATUS.PAUSED:
                    self.button_pause_rob.setText("RESUME")

                elif state == HMICollabApp.STATUS.WORKING:
                    self.button_start_session_rob.setEnabled(False)
                    self.button_pause_rob.setEnabled(True)
                    self.button_end_session_rob.setEnabled(True)

                    self.button_pause_rob.setText("PAUSE")

        @property
        def buttons(self):
            """Returns all the buttons in the layout"""
            return [
                self.button_home,
                self.button_home_rob,
                self.button_measure_label,
                self.button_measure_pcb,
                self.button_start_session,
                self.button_start_session_rob,
                self.button_start_marking,
                self.button_pause,
                self.button_pause_rob,
                self.button_end_session,
                self.button_end_session_rob,
            ]

    # endregion

    def __init__(self):
        super().__init__(name=self.NODE_NAME, depends_list=self.DEPENDS, node_class=ROSNodeCollab)

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
        self.ros_worker.signals.status.connect(self.status_callback)
        self.ros_worker.signals.dependency_online.connect(self.dependency_callback)

        # interface lock variables
        self.__marker_online = False
        self.__robot_online = False
        self.__vision_online = False

        # state machine
        self.__state_rob = None
        self.__state_vis = None

        self.state_robot = HMICollabApp.STATUS.IDLE
        self.state_vision = HMICollabApp.STATUS.IDLE

        # KPI calculation
        self.__kpi_rob = KPI(quota=HMICollabApp.KPI_QUOTA)
        self.__kpi_vis = KPI(quota=HMICollabApp.KPI_QUOTA)

        self.kpi_update_timer = QTimer()
        self.kpi_update_timer.timeout.connect(self.kpi_update_callback)
        self.kpi_update_timer.start(self.KPI_UPDATE_INTERVAL)

    # region OVERRIDES *************************************************************************************************

    def ros_node_online_callback(self):
        """This method gets called whenever a ROS node in the dependency list comes online"""

        if self.ui_locking:  # if ui locking is not disabled
            missing = self.ros_worker.missing_dependencies()  # check for missing dependencies
            if bool(missing):  # the list is not empty
                if NodeList.MARKER_NODE.value not in missing:  # marker is online
                    self.__marker_online = True

                if NodeList.ROBOT2_NODE.value not in missing:  # robot is online
                    self.__robot_online = True

                if not self.__robot_online or not self.__marker_online:  # if either offline, lock
                    self.control_widget.lock_control_robotic(True)

                if NodeList.VISION_NODE.value not in missing:  # vision is online
                    self.__vision_online = True

                if not self.__vision_online:
                    self.control_widget.lock_control_vision(True)

        else:
            logging.info("UI locking is disabled from the command line")

    def ros_error_callback(self, node_name: str, msg: str, err_code: int):
        """This method gets called whenever a ROS node is producing an error"""
        super().ros_error_callback(node_name, msg, err_code)

        # todo differentiate between vision system and robot
        self.info_widget.set_error(HMICollabApp.InfoWidget.VISION, True)

    def clear_errors_callback(self):
        """This method gets called when the 'CLEAR ERRORS' button gets pressed"""
        super().clear_errors_callback()

        self.info_widget.set_error(HMICollabApp.InfoWidget.VISION, False)  # FIXME this may not be needed

    # endregion

    # region CALLBACKS *************************************************************************************************

    def button_clicked_callback(self):
        """Callback method for when a button gets clicked"""
        button_clicked = self.sender()

        # region robotic
        if button_clicked == self.control_widget.button_start_session_rob:
            if self.state_robot == HMICollabApp.STATUS.IDLE:
                self.__kpi_rob = KPI(quota=HMICollabApp.KPI_QUOTA)  # reinit the kpis
                self.__kpi_rob.availability.start_now()

            elif self.state_robot == HMICollabApp.STATUS.WORKING:
                return  # nothing changed, skip

            self.state_robot = HMICollabApp.STATUS.WORKING  # change the state

        elif button_clicked == self.control_widget.button_pause_rob:
            msg = Robot2Control()
            msg.home = False
            msg.start_marking = False
            msg.pause = True

            self.ros_worker.send_control(cell=ROSNodeCollab.ROBOTIC, msg=msg)

            if self.state_robot == HMICollabApp.STATUS.WORKING:
                self.__kpi_rob.performance.pause_start()  # start the pause

                self.state_robot = HMICollabApp.STATUS.PAUSED  # change the state to paused

                return

            if self.state_robot == HMICollabApp.STATUS.PAUSED:
                # resuming from pause
                self.__kpi_rob.performance.pause_end()  # end the pause
                self.state_robot = HMICollabApp.STATUS.WORKING

                return

        elif button_clicked == self.control_widget.button_end_session_rob:
            self.__kpi_rob.availability.end_now()

            self.state_robot = HMICollabApp.STATUS.IDLE

        elif button_clicked == self.control_widget.button_home_rob:
            msg = Robot2Control()
            msg.home = True
            msg.start_marking = False
            msg.pause = False

            self.ros_worker.send_control(cell=ROSNodeCollab.ROBOTIC, msg=msg)

        elif button_clicked == self.control_widget.button_start_marking:
            msg = Robot2Control()
            msg.home = False
            msg.start_marking = True

            self.ros_worker.send_control(cell=ROSNodeCollab.ROBOTIC, msg=msg)

        # endregion

        # region vision
        if button_clicked == self.control_widget.button_start_session:
            if self.state_vision == HMICollabApp.STATUS.IDLE:
                self.__kpi_vis.availability.start_now()

            elif self.state_vision == HMICollabApp.STATUS.WORKING:
                return

            self.state_vision = HMICollabApp.STATUS.WORKING  # change the state

        elif button_clicked == self.control_widget.button_pause:
            if self.state_vision == HMICollabApp.STATUS.WORKING:
                self.__kpi_vis.performance.pause_start()  # start the pause

            elif self.state_vision == HMICollabApp.STATUS.PAUSED:
                # resuming from pause
                self.__kpi_vis.performance.pause_end()
                self.state_vision = HMICollabApp.STATUS.WORKING
                return

            self.state_vision = HMICollabApp.STATUS.PAUSED

        elif button_clicked == self.control_widget.button_end_session:
            self.__kpi_vis.availability.end_now()

            self.state_vision = HMICollabApp.STATUS.IDLE

        elif button_clicked == self.control_widget.button_home:
            msg = VisionControl()
            msg.home = True
            msg.measure_label = False
            msg.measure_pcb = False

            self.ros_worker.send_control(cell=ROSNodeCollab.VISION, msg=msg)

        elif button_clicked == self.control_widget.button_measure_pcb:
            msg = VisionControl()
            msg.home = False
            msg.measure_label = False
            msg.measure_pcb = True

            self.ros_worker.send_control(cell=ROSNodeCollab.VISION, msg=msg)

        elif button_clicked == self.control_widget.button_measure_label:
            msg = VisionControl()
            msg.home = False
            msg.measure_label = True
            msg.measure_pcb = False

            self.ros_worker.send_control(cell=ROSNodeCollab.VISION, msg=msg)

        # endregion

    KPI_PRESCALE = 60  # send ros msg on every 60th visual update

    def kpi_update_callback(self):
        """Updates the KPI readouts on the info widget, and sends it to the OCB with a given prescale"""

        if not hasattr(HMICollabApp.kpi_update_callback, "ticks"):
            raise AttributeError(
                f"The {self.kpi_update_callback.__name__} method must have a 'ticks attribute (initialized to 0)"
            )

        # robotic kpi
        availability = self.__kpi_rob.availability.calculate()
        performance = self.__kpi_rob.performance.calculate(self.__kpi_rob.availability.actual_duration)
        quality = self.__kpi_rob.quality.calculate()

        # display the kpi on the info widget
        self.info_widget.display_kpi(
            self.InfoWidget.ROBOTIC,
            availability=availability,
            quality=quality,
            performance=performance,
        )

        msg = KPIC2()  # create KPI ROS message
        # add the kpis to the message
        msg.availability_robotic = availability
        msg.performance_robotic = performance
        msg.quality_robotic = quality

        # vision kpi
        availability = self.__kpi_vis.availability.calculate()
        performance = self.__kpi_vis.performance.calculate(self.__kpi_vis.availability.actual_duration)
        quality = self.__kpi_vis.quality.calculate()

        # display the kpi on the info widget
        self.info_widget.display_kpi(
            ROSNodeCollab.VISION, availability=availability, quality=quality, performance=performance
        )

        # add the kpi to the ros message
        msg.availability_vision = availability
        msg.performance_vision = performance
        msg.quality_vision = quality

        # if the ticks are larger than the prescale value, send the ros message
        if HMICollabApp.kpi_update_callback.ticks >= HMICollabApp.KPI_PRESCALE:
            # send ROS message
            logging.info("Sending KPI ROS message")
            self.ros_worker.send_kpi(msg)
            HMICollabApp.kpi_update_callback.ticks = 0  # reset the ticks value

        else:
            HMICollabApp.kpi_update_callback.ticks += 1  # increment the ticks

    kpi_update_callback.ticks = 0  # set the method attribute

    # endregion

    # region ROS CALLBACKS *********************************************************************************************

    def status_callback(self, msg):
        """Callback method for the Robot2Status topic messages"""
        if isinstance(msg, Robot2Status):
            self.info_widget.set_error(HMICollabApp.InfoWidget.ROBOTIC, msg.error)
            self.info_widget.set_power(HMICollabApp.InfoWidget.ROBOTIC, msg.power)
            self.info_widget.set_waiting(HMICollabApp.InfoWidget.ROBOTIC, msg.waiting)
            self.info_widget.set_running(HMICollabApp.InfoWidget.ROBOTIC, msg.running)

            if msg.job_success:
                self.__kpi_rob.performance.product_count += 1
                self.__kpi_rob.quality.product_count += 1

            if msg.error:
                self.__kpi_rob.quality.error_count += 1

    def dependency_callback(self, name: str, online: bool):
        """Callback method for when a ROS dependency comes online of goes offline"""
        if name == NodeList.MARKER_NODE.value:
            self.__marker_online = online

        elif name == NodeList.ROBOT2_NODE.value:
            self.__robot_online = online

        elif name == NodeList.VISION_NODE.value:
            self.__vision_online = online

        if not self.ui_locking:
            self.control_widget.lock_control_robotic(False)
            self.control_widget.lock_control_vision(False)

        else:
            if self.__marker_online and self.__robot_online:
                self.logger.info("Unlocking robot UI")
                self.control_widget.lock_control_robotic(False)  # unlock the UI

            else:
                self.logger.info("Locking robot UI")
                self.control_widget.lock_control_robotic(True)

            if self.__vision_online:
                self.logger.info("Unlocking vision UI")
                self.control_widget.lock_control_vision(False)

            else:
                self.logger.info("Locking vision IO")
                self.control_widget.lock_control_vision(True)

    # endregion

    # region PROPERTIES ************************************************************************************************

    @property
    def state_robot(self):
        """Returns the state of the robotic cell"""
        return self.__state_rob

    @state_robot.setter
    def state_robot(self, value: STATUS):
        """Sets the state and locks the buttons accordingly"""
        logging.info(f"Robot state: {value}")
        self.__state_rob = value

        self.control_widget.set_state_robotic(value)

    @property
    def state_vision(self):
        """Returns the state of the vision cell"""
        return self.__state_vis

    @state_vision.setter
    def state_vision(self, value: STATUS):
        """Gets the state and locks the buttons accordingly"""
        self.__state_vis = value

        self.control_widget.set_state_vision(value)

    # endregion


class ROSNodeCollab(QTROSNode):
    """Class for the ROS Node in the HMI application"""

    VISION = 0
    ROBOTIC = 1

    def __init__(self, node_name: str, depends_on: List[str], signals: ROSWorker.Signals):
        super().__init__(node_name=node_name, depends_on=depends_on, signals=signals)

        # publishers
        self.__robot_control = self.create_publisher(
            msg_type=MessageList.ROBOT2_CONTROL.value[1],
            topic=MessageList.ROBOT2_CONTROL.value[0],
            qos_profile=10,
        )

        self.__vision_control = self.create_publisher(
            msg_type=MessageList.VISION_CONTROL.value[1],
            topic=MessageList.VISION_CONTROL.value[0],
            qos_profile=10,
        )

        self.__kpi = self.create_publisher(
            msg_type=MessageList.KPIC2.value[1],
            topic=MessageList.KPIC2.value[0],
            qos_profile=10,
        )

        # subscribers
        self.create_subscription(
            msg_type=MessageList.ROBOT2_STATUS.value[1],
            topic=MessageList.ROBOT2_STATUS.value[0],
            callback=self.robot_status_callback,
            qos_profile=10,
        )

        self.get_logger().info("ROS node online")
        self.signals.started.emit()

    def error_callback(self, msg: Error):
        self.signals.new_error.emit(msg.node_name, msg.error_msg, msg.error_code)

    def all_depends_online(self):
        self.get_logger().info("All dependencies are online")

    def dependency_online(self, name: str, online: bool):
        if online:
            self.get_logger().info(f"A dependency has come online: {name}")

        else:
            self.get_logger().info(f"A dependency has gone offline: {name}")

        self.signals.dependency_online.emit(name, online)

    def dependency_offline(self):
        self.signals.dependency_online.emit("", False)
        self.signals.new_error.emit("Internal error", "A dependency node has gone offline", 0)

    def load_nodes(self):
        self.get_logger().debug("Loading nodes")
        all_nodes = self.dependencies
        missing_nodes = self.missing_dependencies
        self.signals.nodes_loaded.emit(all_nodes, missing_nodes)

    def send_control(self, cell: int, msg: object):
        self.get_logger().debug(f"Sending command: {msg}")
        if cell == self.VISION:
            assert isinstance(msg, VisionControl)
            self.__vision_control.publish(msg)

        elif cell == self.ROBOTIC:
            assert isinstance(msg, Robot2Control)
            self.__robot_control.publish(msg)

        else:
            raise ValueError(f"Invalid cell (number: {cell})")

    def send_kpi(self, msg):
        self.__kpi.publish(msg)

    def robot_status_callback(self, msg: Robot2Status):
        """Callback method for the Robot2Status subscription

        Args:
            msg (Robot2Status): The incoming message
        """
        self.signals.status.emit(msg)


def main(args=None):
    """Entry point for the main function"""
    rclpy.init(args=args)
    try:
        app = QApplication(sys.argv)
        ui_window = HMICollabApp()
        ui_window.show()
        sys.exit(app.exec())
    except KeyboardInterrupt:
        print("Stopping")


if __name__ == "__main__":
    # main()
    main()
