import logging
from multiprocessing.sharedctypes import Value
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import ClassVar

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

import rclpy
from interfaces.msg import Error, Robot2Status, Robot2Control, VisionControl, KPIC2
from mediscara.scripts.hmi import HMIApp, ROSWorker
from mediscara.scripts.ros_node import QTROSNode
from mediscara.config import NodeList, MessageList
from mediscara.scripts.widgets.layout.collab_info_ui import Ui_CollabInfoTab
from mediscara.scripts.widgets.layout.collab_control_ui import Ui_CollabControlWidget


class HMICollabApp(HMIApp):
    NODE_NAME = NodeList.HMINode.value
    DEPENDS = [NodeList.Robot2Node.value, NodeList.MarkerNode.value]

    KPI_UPDATE_INTERVAL = 1000  # ms

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
            super(HMICollabApp.InfoWidget, self).__init__(parent)
            self.setupUi(self)

            self.label_availability_vis.setText("0 %")
            self.label_availability_rob.setText("0 %")
            self.label_performance_vis.setText("0 %")
            self.label_performance_rob.setText("0 %")
            self.label_quality_vis.setText("0 %")
            self.label_quality_rob.setText("0 %")

        def display_kpi(self, box: int, *, availability: float, quality: float, performance: float):
            if box == self.ROBOTIC:
                self.label_availability_rob.setText(f"{availability:.1f}%")
                self.label_quality_rob.setText(f"{quality:.1f}%")
                self.label_performance_rob.setText(f"{performance:.1f}%")

            elif box == self.VISION:
                self.label_availability_vis.setText(f"{availability:.1f}%")
                self.label_quality_vis.setText(f"{quality:.1f}%")
                self.label_performance_vis.setText(f"{performance:.1f}%")

            else:
                raise ValueError(f"Invalid input number ({box})")

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

        def lock_control_vision(self, lock: bool):
            self.button_start_session.setEnabled(not lock)
            self.button_home.setEnabled(not lock)
            self.button_measure_label.setEnabled(not lock)
            self.button_measure_pcb.setEnabled(not lock)

        def lock_control_robotic(self, lock: bool):
            self.button_start_session_rob.setEnabled(not lock)
            self.button_home_rob.setEnabled(not lock)
            self.button_start_marking.setEnabled(not lock)

        @property
        def buttons(self):
            return [self.button_home,
                    self.button_home_rob,
                    self.button_measure_label,
                    self.button_measure_pcb,
                    self.button_start_session,
                    self.button_start_session_rob,
                    self.button_start_marking,
                    self.button_pause,
                    self.button_pause_rob,
                    self.button_end_session,
                    self.button_end_session_rob]

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

        # KPI calculation
        self.__kpi_rob = KPI()
        self.__kpi_vis = KPI()

        self.kpi_update_timer = QTimer()
        self.kpi_update_timer.timeout.connect(self.kpi_update_callback)
        self.kpi_update_timer.start(self.KPI_UPDATE_INTERVAL)

    # region OVERRIDES *************************************************************************************************

    def ros_node_online_callback(self):
        self.logger.debug("ROS Node online")

        if self.ui_locking:  # if ui locking is not disabled
            missing = self.ros_worker.missing_dependencies()  # check for missing dependencies
            if bool(missing):  # the list is not empty
                if NodeList.MarkerNode.value not in missing:  # marker is online
                    self.__marker_online = True

                if NodeList.Robot2Node.value not in missing:  # robot is online
                    self.__robot_online = True

                if not self.__robot_online or not self.__marker_online:  # if either offline, lock
                    self.control_widget.lock_control_robotic(True)

                if not self.__vision_online:
                    self.control_widget.lock_control_vision(True)

                # todo finish the vision system nodes

        else:
            logging.info("UI locking is disabled from the command line")

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

        # robotic
        if button_clicked == self.control_widget.button_start_session_rob:
            if self.state_robot == HMICollabApp.STATUS.IDLE:
                self.__kpi_rob.availability.start_now()

            elif self.state_robot == HMICollabApp.STATUS.WORKING:
                return  # nothing changed, skip

            self.state_robot = HMICollabApp.STATUS.WORKING  # change the state

        elif button_clicked == self.control_widget.button_pause_rob:
            if self.state_robot == HMICollabApp.STATUS.WORKING:
                self.__kpi_rob.performance.pause_start()  # start the pause

            elif self.state_robot == HMICollabApp.STATUS.PAUSED:
                # resuming from pause
                self.__kpi_rob.performance.pause_end()  # end the pause
                self.state_robot = HMICollabApp.STATUS.WORKING
                return

            self.state_robot = HMICollabApp.STATUS.PAUSED  # change the state to paused

        elif button_clicked == self.control_widget.button_end_session_rob:
            self.__kpi_rob.availability.end_now()
            
            self.state_robot = HMICollabApp.STATUS.IDLE

    def kpi_update_callback(self):
        a = self.__kpi_rob.availability.calculate()
        p = self.__kpi_rob.performance.calculate(self.__kpi_rob.availability.actual_duration)
        q = self.__kpi_rob.quality.calculate()

        self.info_widget.display_kpi(
            self.InfoWidget.ROBOTIC,
            availability=self.__kpi_rob.availability.calculate(),
            quality=self.__kpi_rob.quality.calculate(),
            performance=self.__kpi_rob.performance.calculate(self.__kpi_rob.availability.actual_duration)
        )

        msg = KPIC2()
        msg.availability = a
        msg.performance = p
        msg.quality = q

        logging.info("Sending ROS MSG")
        self.ros_worker.send_kpi(ROSNodeCollab.ROBOTIC, msg)

        self.kpi_update_timer.start(self.KPI_UPDATE_INTERVAL)  # restart timer

    # endregion

    # region ROS CALLBACKS *********************************************************************************************

    def status_callback(self, msg):
        if isinstance(msg, Robot2Status):
            self.info_widget.set_error(HMICollabApp.InfoWidget.ROBOTIC, msg.error)
            self.info_widget.set_power(HMICollabApp.InfoWidget.ROBOTIC, msg.power)
            self.info_widget.set_waiting(HMICollabApp.InfoWidget.ROBOTIC, msg.waiting)
            self.info_widget.set_running(HMICollabApp.InfoWidget.ROBOTIC, msg.running)

    def dependency_callback(self, name: str, online: bool):
        if name == NodeList.MarkerNode.value:
            self.__marker_online = online

        elif name == NodeList.Robot2Node.value:
            self.__robot_online = online

        # todo implement vision system

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
        return self.__state_rob

    @state_robot.setter
    def state_robot(self, value: STATUS):
        """Sets the state and locks the buttons accordingly"""
        self.__state_rob = value
        logging.info(f"Status set to: {value}")

        if value == HMICollabApp.STATUS.IDLE:
            self.control_widget.button_start_session_rob.setEnabled(True)
            self.control_widget.button_pause_rob.setEnabled(False)
            self.control_widget.button_end_session_rob.setEnabled(False)

            self.control_widget.button_pause_rob.setText("PAUSE")

        elif value == HMICollabApp.STATUS.PAUSED:
            self.control_widget.button_pause_rob.setText("RESUME")

        elif value == HMICollabApp.STATUS.WORKING:
            self.control_widget.button_start_session_rob.setEnabled(False)
            self.control_widget.button_pause_rob.setEnabled(True)
            self.control_widget.button_end_session_rob.setEnabled(True)

            self.control_widget.button_pause_rob.setText("PAUSE")

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

        self.__kpi_robotic = self.create_publisher(
            msg_type=MessageList.KPIC2.value[1],
            topic=MessageList.KPIC2.value[0],
            qos_profile=10
            )

        # subscribers
        self.__robot_status_subscription = self.create_subscription(
            msg_type=MessageList.Robot2Status.value[1],
            topic=MessageList.Robot2Status.value[0],
            callback=self.robot_status_callback,
            qos_profile=10
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

    def depends_offline(self):
        self.signals.dependency_online.emit("", False)
        self.signals.new_error.emit("Internal error", "A dependency node has gone offline", 0)

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

    def send_kpi(self, cell: int, msg):
        self.get_logger().info(f"Sending message: {msg}")
        if cell == self.VISION:
            raise NotImplementedError

        elif cell == self.ROBOTIC:
            self.__kpi_robotic.publish(msg)

        else:
            raise ValueError(f"Invalid cell (numer: {cell})")

    def robot_status_callback(self, msg: Robot2Status):
        self.signals.status.emit(msg)


class KPI:
    """Class for tracking and managing KPIs"""

    PRODUCT_QUOTA = 60

    def __init__(self):
        self.__availability = KPI.Availability()
        self.__quality = KPI.Quality(self.PRODUCT_QUOTA)
        self.__performance = KPI.Performance(self.PRODUCT_QUOTA)

    @property
    def availability(self):
        return self.__availability

    @property
    def quality(self):
        return self.__quality

    @property
    def performance(self):
        return self.__performance

    @dataclass
    class Availability:
        format = "%H:%M:%S"
        __planned_start: ClassVar[datetime] = datetime.strptime("08:00:00", format)
        __planned_end: ClassVar[datetime] = datetime.strptime("8:03:00", format)

        __actual_start: datetime = field(default=None)
        __actual_end: datetime = field(default=None)

        def __str__(self):
            if self.actual_start is None:
                actual_start_str = "Not started yet"
            else:
                actual_start_str = self.__actual_start.strftime(self.format)

            if self.__actual_end is None:
                actual_end_str = "Not ended yet"
            else:
                actual_end_str = self.__actual_end.strftime(self.format)

            return f"planned start: {self.__planned_start.strftime(self.format)} " \
                   f"planned start: {self.__planned_start.strftime(self.format)} " \
                   f"actual start: {actual_start_str} " \
                   f"actual end: {actual_end_str}"

        def start_now(self):
            self.__actual_start = datetime.now()

        def end_now(self):
            self.__actual_end = datetime.now()

        def calculate(self):
            planned_duration = self.__planned_end - self.__planned_start

            return self.actual_duration / planned_duration

        # region PROPERTIES

        @property
        def actual_start(self):
            if self.__actual_start is None:
                return "Not set yet"
            else:
                return self.__actual_start.strftime(self.format)

        @property
        def actual_end(self):
            if self.__actual_end is None:
                return "Not set yet"
            else:
                return self.__actual_end

        @property
        def planned_start(self):
            return self.__planned_start

        @property
        def planned_end(self):
            return self.__planned_end

        @property
        def actual_duration(self) -> timedelta:
            """Returns the actual duration (A_curM in the documenatation)"""
            if self.__actual_start is None:
                return timedelta(0)

            start = self.__actual_start

            if self.__actual_end is None:
                end = datetime.now()

            else:
                end = self.__actual_end

            return end - start

        # endregion

    @dataclass
    class Quality:
        """Class for calculating and storing quality KPI data

        Reference quality is defined as
        """

        __product_quota: int

        __product_count: int = field(default=0)
        __error_count: int = field(default=0)

        def calculate(self):
            return (self.product_count - self.error_count) / self.__product_quota

        @property
        def product_count(self):
            return self.__product_count

        @product_count.setter
        def product_count(self, value: int):
            self.__product_count = value

        @property
        def error_count(self):
            return self.__error_count

        @error_count.setter
        def error_count(self, value: int):
            self.__error_count = value

    @dataclass
    class Performance:
        """Class for calculating and storing performance KPIs

        Performance is calculated as {products manufactured} / {manufacturing time}
        Reference performance is 60 [-] / 10 [h]
        Actual performance is calculated as {actual products made} / A_curM - {time paused}
            - where A_curM is the actual working time (see Availability class)

        The performance KPI is calculated like this:
            - P_M = {Actual performance} / {Reference performance}

        To simplify code performance will be calculated as
            - {manufacturing time} / {products manufactured}
        and the performance KPI will be calculated as
            - 1 / P_M = 1 / ({Actual performance} / {Reference performance})
        """
        __product_quota: int

        __work_period: ClassVar[timedelta] = timedelta(hours=10)
        __reference_performance: timedelta = field(init=False)

        __paused: timedelta = field(default=timedelta(0))
        __pause_timer: ClassVar[datetime] = None

        __product_count: int = field(default=0)

        def __post_init__(self):
            self.__reference_performance = self.__work_period / self.__product_quota

        def calculate(self, a_cur_m: timedelta):
            if self.product_count == 0:
                return 0.00

            actual_performance = (a_cur_m - self.paused) / self.product_count

            if actual_performance == timedelta(0):
                return 0.0

            return self.__reference_performance / actual_performance

        def pause_start(self):
            self.__pause_timer = datetime.now()

        def pause_end(self):
            if self.__pause_timer is None:
                return

            self.paused += datetime.now() - self.__pause_timer
            self.__pause_timer = None

        @property
        def paused(self):
            return self.__paused

        @paused.setter
        def paused(self, value: timedelta):
            self.__paused = value

        @property
        def product_count(self):
            return self.__product_count

        @product_count.setter
        def product_count(self, value: int):
            self.__product_count = value


def main(args=None):
    rclpy.init(args=args)
    try:
        app = QApplication(sys.argv)
        ui_window = HMICollabApp()
        ui_window.show()
        sys.exit(app.exec())
    except KeyboardInterrupt:
        print("Stopping")


def t():
    import time
    avail = HMICollabApp.KPI.Availability()
    avail.start_now()
    time.sleep(1)
    avail.end_now()
    print(avail)


if __name__ == '__main__':
    # main()
    main()
