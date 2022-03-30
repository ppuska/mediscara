import enum
import sys
from typing import List, Type

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread, QMutex, QUrl, Qt
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QLabel, QListWidget, QListWidgetItem, QWidget

import rclpy
from mediscara.scripts.ros_node import QTROSNode
from mediscara.config import IPList
from mediscara.scripts.widgets.layout.gui_ui import Ui_GUIWindow
from mediscara.scripts.widgets.layout.error_list_item_ui import Ui_ErrorListItem
from mediscara.scripts.widgets.layout.node_list_item_ui import Ui_NodeListItem
from mediscara.scripts.logger import Logger

from mediscara.scripts.widgets.layout.statusbar_ui import Ui_StatusBar


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

    __NO_LOGIN = "--nologin"
    __NO_LOCK = "--nolock"

    # region INNER CLASSES *********************************************************************************************

    class ErrorListItem(Ui_ErrorListItem, QWidget):
        def __init__(self, node_name: str, error_msg: str, error_code: int):
            super(HMIApp.ErrorListItem, self).__init__()
            self.setupUi(self)
            self.label_node_name.setText(node_name)
            self.label_error_message.setText(error_msg)
            self.label_error_code.setText(str(error_code))

    class NodeListItem(Ui_NodeListItem, QWidget):

        __STYLESHEET = "padding: 12px; border: 1px solid black; border-radius: 7px; "

        def __init__(self, node_name: str, missing: bool):
            super(HMIApp.NodeListItem, self).__init__()
            self.setupUi(self)

            self.label_node_name.setText(node_name)
            self.missing = missing
            if missing:
                self.label_node_name.setStyleSheet(self.__STYLESHEET + "background-color: yellow")
            else:
                self.label_node_name.setStyleSheet(self.__STYLESHEET + "background-color: green")

        def __repr__(self):
            return f"{self.__class__.__name__}({self.label_node_name.text()}, {self.missing})"

    class StatusbarWidget(Ui_StatusBar, QWidget):
        def __init__(self):
            super(HMIApp.StatusbarWidget, self).__init__()
            self.setupUi(self)

            self.label_login.setText("Not logged in")
            self.set_error_count(0)

        def set_error_count(self, err_count: int):
            if err_count == 0:
                self.label_error.setStyleSheet("background-color: white")
                self.label_error.setText("No errors")
            else:
                self.label_error.setStyleSheet("background-color: red;")
                if err_count == 1:
                    self.label_error.setText("1 error")

                else:
                    self.label_error.setText(f"{err_count} errors")

    # endregion

    def __init__(self, name: str, depends_list: List[str], node_class: Type[QTROSNode]):
        """Constructor method

        :param name: the name of the ROS node in the app
        :param depends_list: a list of ROS node names on which this ROS node depends
        :param node_class: Class object derived from the QTROSNode base class, which gets initialized and
        communicates with the user interface
        """
        super(HMIApp, self).__init__()
        self.setupUi(self)

        self.logger = Logger(parent=None, tag="HMI", level=Logger.DEBUG)

        self.__user_level = None

        """ Create ROS thread """
        self.ros_thread = QThread()  # create thread

        self.ros_worker = ROSWorker(node_class=node_class,
                                    node_name=name,
                                    depends_list=depends_list
                                    )

        self.ros_worker.add_to_thread(self.ros_thread)

        # connect the signals and slots
        self.ros_worker.signals.started.connect(self.ros_node_online_callback)
        self.ros_worker.signals.nodes_loaded.connect(self.nodes_loaded_callback)
        self.ros_worker.signals.info_loaded.connect(self.info_loaded_callback)
        self.ros_worker.signals.new_error.connect(self.ros_error_callback)

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
        self.button_clear_errors.clicked.connect(self.clear_errors_callback)

        """Set up the statusbar widget for login info"""
        self.statusbar_widget = HMIApp.StatusbarWidget()
        self.statusbar.addPermanentWidget(self.statusbar_widget, stretch=1)

        """Set up login level"""
        # command line arguments
        if sys.argv is not None:
            print(sys.argv)
            if self.__NO_LOGIN in sys.argv:
                # no login mode
                self.user_level = LoginStatus.ADMIN

            else:
                self.user_level = LoginStatus.LOGGED_OUT

            if self.__NO_LOCK in sys.argv:
                self.ui_locking = False

            else:
                self.ui_locking = True

        self.logger.info("Base class constructor done")

    # region OVERRIDES *************************************************************************************************

    def closeEvent(self, event) -> None:
        self.ros_worker.stop()
        self.ros_thread.quit()
        self.ros_thread.wait()

    # endregion

    # region ROS CALLBACKS *********************************************************************************************

    def ros_node_online_callback(self):
        pass

    def nodes_loaded_callback(self, dependencies: List[str], missing: List[str]):
        """Callback method for displaying the loaded nodes"""

        self.list_nodes.clear()  # clear the nodes list

        for row, node in enumerate(dependencies):  # iterate through the dependency nodes
            item_widget = HMIApp.NodeListItem(node, missing=(node in missing))
            list_widget_item = QListWidgetItem(self.list_nodes)  # add a new list widget item
            list_widget_item.setSizeHint(item_widget.sizeHint())  # copy the size hint from the item widget
            self.list_nodes.addItem(list_widget_item)
            self.list_nodes.setItemWidget(list_widget_item, item_widget)

    def info_loaded_callback(self):
        """Callback method for consuming the KPI info returned by the ROS thread"""
        pass

    def ros_error_callback(self, node_name: str, msg: str, err_code: int):
        item_widget = HMIApp.ErrorListItem(node_name=node_name, error_msg=msg, error_code=err_code)
        list_widget_item = QListWidgetItem(self.list_error)  # add a new list widget item
        list_widget_item.setSizeHint(item_widget.sizeHint())  # copy the size hint from the item widget
        self.list_error.addItem(list_widget_item)   # add a new item
        self.list_error.setItemWidget(list_widget_item, item_widget)  # set the item widget to the item

        self.statusbar_widget.set_error_count(self.list_error.count())

    # endregion

    # region CALLBACKS *************************************************************************************************

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
                self.label_login.setText("")

            else:
                self.label_login.setText("Invalid password")

        except KeyError:
            self.label_login.setText("Invalid username")

    def logout_callback(self):
        """This method gets called when the logout button is pressed"""
        self.user_level = LoginStatus.LOGGED_OUT

    def clear_errors_callback(self):
        """Callback method for the 'CLEAR ERRORS' button"""
        self.list_error.clear()
        self.statusbar_widget.set_error_count(0)

    # endregion

    # region METHODS ***************************************************************************************************

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
            self.tabWidget.setTabEnabled(0, True)  # info locked
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

    # endregion

    # region PROPERTIES ************************************************************************************************

    @property
    def user_level(self):
        return self.__user_level

    @user_level.setter
    def user_level(self, value: LoginStatus):
        self.__user_level = value
        if value == LoginStatus.LOGGED_OUT:
            self.statusbar_widget.label_login.setText(f"Not signed in")

        else:
            self.statusbar_widget.label_login.setText(f"Signed in as {value.value}")

        self.set_interface_lock()

    # endregion


class ROSWorker(QObject):
    """Class to implement a Worker object to manage thread-safe interaction between the ROS node and the GUI"""

    mutex = QMutex()

    """ SIGNALS """
    finished = pyqtSignal()

    """ SIGNALS FOR THE ROS NODE """

    class Signals(QObject):
        started = pyqtSignal()
        nodes_loaded = pyqtSignal(list, list)
        info_loaded = pyqtSignal()
        new_error = pyqtSignal(str, str, int)
        dependency_online = pyqtSignal(str, bool)
        kpi = pyqtSignal(object)
        status = pyqtSignal(object)

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
    def send_control(self, *args, **kwargs):
        assert isinstance(self.__ros_node, QTROSNode)
        self.__ros_node.send_control(*args, **kwargs)

    @pyqtSlot()
    def stop(self):
        self.__ros_node.get_logger().info("Shutting down ROS node")
        rclpy.shutdown()
        self.finished.emit()

    @pyqtSlot()
    def missing_dependencies(self):
        self.mutex.lock()
        missing = self.__ros_node.missing_dependencies
        self.mutex.unlock()

        return missing

    @property
    def signals(self):
        return self.__signals

    @property
    def ready(self):
        """Returns if the ROS node is properly initialized"""
        return self.__ready
