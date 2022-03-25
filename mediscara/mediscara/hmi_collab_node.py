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
        pass

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


# class HMICollabApp(QMainWindow, Ui_GUIWindow):
#     """Class for displaying a Qt window"""
#
#     __TAB_INFO = 0
#     __TAB_CONTROL = 1
#     __TAB_NODES = 2
#     __TAB_GRAFANA = 3
#     __TAB_ERROR = 4
#     __TAB_LOGIN = 5
#
#     __TAB_SIZE = (50, 100)
#
#     def __init__(self):
#         super(HMICollabApp, self).__init__()
#         self.setupUi(self)
#
#         self.__user_level = LoginStatus.LOGGED_OUT
#
#         """Create ROS task"""
#         # create thread
#         self.ros_thread = QThread()
#         # create worker
#         self.ros_worker = Worker()
#         # move the worker to the thread
#         self.ros_worker.moveToThread(self.ros_thread)
#         # connect signals and slots
#         self.ros_thread.started.connect(self.ros_worker.run)
#         self.ros_worker.finished.connect(self.ros_thread.quit)
#         self.ros_worker.finished.connect(self.ros_worker.deleteLater)
#         self.ros_thread.finished.connect(self.ros_thread.deleteLater)
#         # custom signals
#         self.ros_worker.started.connect(self.ros_node_online_callback)
#
#         # start the thread
#         self.ros_thread.start()
#
#         self.tabWidget.currentChanged.connect(self.tab_changed_callback)
#
#         """Init the tabs"""
#         self.tabWidget.setCurrentIndex(0)  # reset current index
#         self.load_info()
#
#         """LOGIN tab"""
#         self.button_login.clicked.connect(self.login_callback)
#         self.button_logout.clicked.connect(self.logout_callback)
#         self.label_login.setText("")
#
#         """NODES tab"""
#         self.button_refresh.clicked.connect(self.load_nodes)
#         self.ros_worker.nodes_loaded.connect(self.nodes_loaded)
#
#         """Set up the statusbar widget for login info"""
#         self.statusbar_label = QLabel()
#         self.statusbar_label.setText("Not logged in")
#         self.statusbar.addWidget(self.statusbar_label)
#
#     def closeEvent(self, event):
#         self.ros_worker.stop()
#         self.ros_thread.quit()
#         self.ros_thread.wait()
#
#     def ros_node_online_callback(self):
#         pass
#
#     def ros_node_offline_callback(self):
#         statusbar_label = QLabel()
#         statusbar_label.setText("ROS is offline")
#         self.statusbar.addWidget(statusbar_label)
#
#     """ TABS --------------------------------------------------------------------------------------------------------"""
#
#     def tab_changed_callback(self, index: int):
#         """Callback function for when the current selected tab changes"""
#         if index == self.__TAB_INFO:
#             pass
#
#         elif index == self.__TAB_CONTROL:
#             pass
#
#         elif index == self.__TAB_NODES:
#             self.load_nodes()
#
#         elif index == self.__TAB_GRAFANA:
#             pass
#
#         elif index == self.__TAB_ERROR:
#             pass
#
#         elif index == self.__TAB_LOGIN:
#             pass
#
#     def load_info(self):
#         pass  # todo implement this
#
#     def load_nodes(self):
#         self.ros_worker.load_nodes()
#
#     def nodes_loaded(self, all_nodes: list, missing_nodes: list):
#         self.table_nodes.setRowCount(len(all_nodes))  # set the row number
#
#         for row, node in enumerate(all_nodes):  # iterate through the dependency nodes
#             self.table_nodes.setItem(row, 0, QTableWidgetItem(node))
#
#             if node in missing_nodes:
#                 text = "Offline"
#             else:
#                 text = "Online"
#
#             self.table_nodes.setItem(row, 1, QTableWidgetItem(text))
#
#     def login_callback(self):
#         name = self.line_edit_name.text()
#         passwd = self.line_edit_pass.text()
#
#         try:
#             level = LoginStatus(name)  # gets the login level /USER ADMIN MAINTENANCE/ or throws KeyError
#             if passwd == LoginStatus.get_pass(level):  # if the password for the level is matching
#                 self.__user_level = level
#                 self.statusbar_label.setText(f"Signed in as {level.name}")
#                 self.label_login.setText("")
#
#             else:
#                 self.label_login.setText("Invalid password")
#
#         except KeyError:
#             self.label_login.setText("Invalid username")
#
#     def logout_callback(self):
#         self.__user_level = LoginStatus.LOGGED_OUT
#         self.statusbar_label.setText("Not logged in")
#
#     def node_list(self):
#         pass


# class ROSNode(CellNode):
#
#     def __init__(self, started_callback, info_loaded_callback, nodes_loaded_callback):
#         super(ROSNode, self).__init__(
#             node_name=NodeList.HMINode.value,
#             depends_on=[
#                 NodeList.Robot2Node.value,
#                 NodeList.MarkerNode.value
#             ]
#         )
#
#         self.__nodes_loaded_callback = nodes_loaded_callback
#         self.get_logger().info("ROS Node online")
#         started_callback()
#
#     def status_callback(self, msg):
#         pass
#
#     def error_callback(self, msg: Error):
#         pass
#
#     def depends_online(self):
#         pass
#
#     def depends_offline(self):
#         pass
#
#     def load_info(self):
#         pass
#
#     def load_nodes(self):
#         all_nodes = self.dependencies
#         missing_nodes = self.missing_dependencies
#         self.__nodes_loaded_callback(all_nodes, missing_nodes)


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
