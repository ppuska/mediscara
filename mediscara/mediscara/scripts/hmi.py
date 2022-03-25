import enum
import sys
from abc import abstractmethod
from typing import List, Type

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread, QMutex, QUrl
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QLabel, QApplication


import rclpy
from .ros_node import QTROSNode
from .utils import IPList

from .widgets.layout.gui_UI import Ui_GUIWindow


class LoginStatus(enum.Enum):
    """Class for storing login statuses

    Manager - INFO GRAFANA
    Admin - ALL
    User - CONTROL INFO
    """
    LOGGED_OUT = None
    USER = "user"
    ADMIN = "admin"
    MANAGER = "manager"

    __USER_PASS = "user"
    __ADMIN_PASS = "admin"
    __MANAGER_PASS = "manager"

    @classmethod
    def get_pass(cls, lvl):
        """Returns the selected user's password"""
        if lvl == cls.LOGGED_OUT:
            return None
        elif lvl == cls.USER:
            return cls.__USER_PASS.value
        elif lvl == cls.ADMIN:
            return cls.__ADMIN_PASS.value
        elif lvl == cls.MANAGER:
            return cls.__MANAGER_PASS.value


# noinspection PyUnresolvedReferences
class HMIApp(QMainWindow, Ui_GUIWindow):
    """Base class for the HMI interfaces of the robotic cells"""

    __TAB_INFO = 0
    __TAB_CONTROL = 1
    __TAB_NODES = 2
    __TAB_GRAFANA = 3
    __TAB_ERROR = 4
    __TAB_LOGIN = 5

    def __init__(self, name: str, depends_list: List[str], node_class: Type[QTROSNode]):
        """Constructor method

        :param name: the name of the ROS node in the app
        :param depends_list: a list of ROS node names on which this ROS node depends
        :param node_class: Class object derived from the QTROSNode base class, which gets initialized and
        communicates with the user interface
        """
        super(HMIApp, self).__init__()
        self.setupUi(self)

        """ Create ROS thread """
        self.ros_thread = QThread()  # create thread

        if node_class is not None:
            self.ros_worker = ROSWorker(node_class=node_class,
                                        node_name=name,
                                        depends_list=depends_list
                                        )

            self.ros_worker.add_to_thread(self.ros_thread)

            # connect the signals and slots
            self.ros_worker.signals.nodes_loaded.connect(self.nodes_loaded_callback)
            self.ros_worker.signals.info_loaded.connect(self.info_loaded_callback)

            self.ros_thread.start()  # start the thread

        """ Create callbacks """
        self.tabWidget.currentChanged.connect(self.tab_changed_callback)

        """ Tabs initialization """
        self.tabWidget.setCurrentIndex(self.__TAB_LOGIN)  # login screen

        # login tab
        self.button_login.clicked.connect(self.login_callback)
        self.button_logout.clicked.connect(self.logout_callback)

        # nodes tab
        self.button_refresh.clicked.connect(self.load_nodes)

        # grafana tab
        self.web_widget.load(QUrl(IPList.Grafana.value))
        self.web_widget.show()

        # error tab

        """Set up the statusbar widget for login info"""
        self.statusbar_label = QLabel()
        self.statusbar_label.setText("Not logged in")
        self.statusbar.addWidget(self.statusbar_label)

        """Set up login level"""
        self.__user_level = LoginStatus.LOGGED_OUT
        self.set_interface_lock()

    """ OVERRIDES ************************************************************************************************** """

    def closeEvent(self, event) -> None:
        self.ros_worker.stop()
        self.ros_thread.quit()
        self.ros_thread.wait()

    """ ROS CALLBACKS ********************************************************************************************** """

    def nodes_loaded_callback(self, dependencies: List[str], missing: List[str]):
        """Callback method for displaying the loaded nodes"""
        self.table_nodes.setRowCount(len(dependencies))  # set the row number

        for row, node in enumerate(dependencies):  # iterate through the dependency nodes
            self.table_nodes.setItem(row, 0, QTableWidgetItem(node))

            if node in missing:
                text = "Offline"
            else:
                text = "Online"

            self.table_nodes.setItem(row, 1, QTableWidgetItem(text))

    def info_loaded_callback(self):
        """Callback method for consuming the KPI info returned by the ROS thread"""
        pass

    """ CALLBACKS ************************************************************************************************** """

    def tab_changed_callback(self, index: int):
        """Callback function for when the current selected tab changes"""
        if index == self.__TAB_INFO:
            pass

        elif index == self.__TAB_CONTROL:
            pass

        elif index == self.__TAB_NODES:
            self.ros_worker.load_nodes()

        elif index == self.__TAB_GRAFANA:
            pass
            # self.web_widget.load(QUrl(IPList.Grafana.value))
            # self.web_widget.show()

        elif index == self.__TAB_ERROR:
            pass

        elif index == self.__TAB_LOGIN:
            pass

    def login_callback(self):
        """This method gets called when the login button gets pressed"""
        name = self.line_edit_name.text()
        passwd = self.line_edit_pass.text()

        try:
            level = LoginStatus(name)  # gets the login level /USER ADMIN MAINTENANCE/ or throws KeyError
            if passwd == LoginStatus.get_pass(level):  # if the password for the level is matching
                self.user_level = level
                self.statusbar_label.setText(f"Signed in as {level.name}")
                self.label_login.setText("")

            else:
                self.label_login.setText("Invalid password")

        except KeyError:
            self.label_login.setText("Invalid username")

    def logout_callback(self):
        """This method gets called when the logout button is pressed"""
        self.user_level = LoginStatus.LOGGED_OUT
        self.statusbar_label.setText("Not logged in")

    """ METHODS **************************************************************************************************** """

    def load_nodes(self):
        self.ros_worker.load_nodes()

    def load_info(self):
        self.ros_worker.load_info()

    def set_interface_lock(self):
        """Locks the interface elements according to the user level"""
        if self.user_level == LoginStatus.LOGGED_OUT:
            self.tabWidget.setTabEnabled(0, False)  # info locked
            self.tabWidget.setTabEnabled(1, False)  # control locked
            self.tabWidget.setTabEnabled(2, True)  # nodes enabled
            self.tabWidget.setTabEnabled(3, False)  # grafana locked
            self.tabWidget.setTabEnabled(4, True)  # error log enabled
            self.tabWidget.setTabEnabled(5, True)  # login tab enabled

        elif self.user_level == LoginStatus.USER:
            self.tabWidget.setTabEnabled(0, True)  # info enabled
            self.tabWidget.setTabEnabled(1, True)  # control enabled
            self.tabWidget.setTabEnabled(2, True)  # nodes enabled
            self.tabWidget.setTabEnabled(3, False)  # grafana locked
            self.tabWidget.setTabEnabled(4, True)  # error log enabled
            self.tabWidget.setTabEnabled(5, True)  # login tab enabled

        elif self.user_level == LoginStatus.MANAGER:
            self.tabWidget.setTabEnabled(0, False)  # info locked
            self.tabWidget.setTabEnabled(1, False)  # control locked
            self.tabWidget.setTabEnabled(2, True)  # nodes enabled
            self.tabWidget.setTabEnabled(3, True)  # grafana enabled
            self.tabWidget.setTabEnabled(4, True)  # error log enabled
            self.tabWidget.setTabEnabled(5, True)  # login tab enabled

        elif self.user_level == LoginStatus.ADMIN:
            self.tabWidget.setTabEnabled(0, True)  # info enabled
            self.tabWidget.setTabEnabled(1, True)  # control enabled
            self.tabWidget.setTabEnabled(2, True)  # nodes enabled
            self.tabWidget.setTabEnabled(3, True)  # grafana enabled
            self.tabWidget.setTabEnabled(4, True)  # error log enabled
            self.tabWidget.setTabEnabled(5, True)  # login tab enabled

    """ PROPERTIES ************************************************************************************************* """

    @property
    def user_level(self):
        return self.__user_level

    @user_level.setter
    def user_level(self, value: LoginStatus):
        self.__user_level = value
        self.set_interface_lock()


class ROSWorker(QObject):
    """Class to implement a Worker object to manage thread-safe interaction between the ROS node and the GUI"""

    mutex = QMutex()

    """ SIGNALS """
    started = pyqtSignal()
    finished = pyqtSignal()

    """ SIGNALS FOR THE ROS NODE """

    class Signals(QObject):
        nodes_loaded = pyqtSignal(list, list)
        info_loaded = pyqtSignal()

    def __init__(self,
                 node_class: Type[QTROSNode],
                 node_name: str,
                 depends_list: List[str]
                 ):
        super(ROSWorker, self).__init__()
        self.__node_class = node_class
        self.__ros_node = None
        self.__node_name = node_name
        self.__depends_list = depends_list
        self.__signals = ROSWorker.Signals()

        self.__ready = False

    # noinspection PyUnresolvedReferences
    def add_to_thread(self, thread: QThread):
        """Adds the worker object to the thread"""
        self.moveToThread(thread)
        thread.started.connect(self.run)
        self.finished.connect(thread.quit)
        self.finished.connect(self.deleteLater)
        self.finished.connect(thread.deleteLater)

    def run(self):
        """Task for running the ROS node"""
        self.__ros_node = self.__node_class(node_name=self.__node_name,
                                            depends_on=self.__depends_list,
                                            signals=self.signals
                                            )
        rclpy.spin(self.__ros_node)

        self.mutex.lock()
        self.__ready = True
        self.mutex.unlock()

    @abstractmethod
    @pyqtSlot()
    def load_info(self):
        """Loads the info to the INFO tab of the hmi"""
        print(self.ready)
        self.__ros_node.load_info()

    @pyqtSlot()
    def load_nodes(self):
        assert isinstance(self.__ros_node, QTROSNode)
        self.__ros_node.load_nodes()

    @pyqtSlot()
    def send_control(self):
        assert isinstance(self.__ros_node, QTROSNode)
        self.__ros_node.send_control()

    @pyqtSlot()
    def stop(self):
        self.__ros_node.get_logger().info("Shutting down ROS node")
        rclpy.shutdown()
        self.finished.emit()

    @property
    def signals(self):
        return self.__signals

    @property
    def ready(self):
        """Returns if the ROS node is properly initialized"""
        return self.__ready
