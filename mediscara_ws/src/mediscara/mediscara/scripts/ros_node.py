"""Library module for the Base ROS Node class"""
from typing import List
from abc import ABC, abstractmethod

from rclpy.node import Node

from interfaces.msg import Error
from mediscara.scripts.utils import ErrorClass as UtilsError




class ROSNode(Node, ABC):
    """Class for a ROS node for a robot cell"""

    __DEPENDENCY_CHECK_INTERVAL = 1  # s

    def __init__(self, node_name: str, depends_on=None):
        """Initialization method

        :returns: None
        :param node_name the name of the node
        :param depends_on list of nodes on which this node depends
        :type node_name str
        :type depends_on list(str)
        """
        super(ROSNode, self).__init__(f"{node_name}_node")

        # Create dependency check
        self.__dependencies = depends_on
        self.__missing_depends_prev_state = None
        self.__missing_depends_prev = None
        self.__depends_timer = self.create_timer(ROSNode.__DEPENDENCY_CHECK_INTERVAL, self.__depends_callback)

        if not self.dependencies_ok:
            missing = self.missing_dependencies
            self.get_logger().warn(f"Missing dependency nodes: \n{missing}")
            self.__missing_depends_prev_state = True
            self.__missing_depends_prev = missing

        else:
            self.__missing_depends_prev_state = False
            self.__missing_depends_prev = []

        # Create error and status subscription on dependencies
        if self.__dependencies is not None:
            for node in self.__dependencies:
                # error
                self.create_subscription(
                    msg_type=Error,
                    topic=f"{node}_error",
                    callback=self.error_callback,
                    qos_profile=10
                )

                self.get_logger().debug(f'Error subscription for node "{node}" created')

        # Create error publisher
        self.__error_publisher = self.create_publisher(
            msg_type=Error,
            topic=f'{node_name}_error',
            qos_profile=10
        )

    # region CALLBACKS -------------------------------------------------------------------------------------------------

    def __depends_callback(self):
        """Checks is the missing dependencies have come online"""
        # check if a single dependency has come online
        if self.missing_dependencies != self.__missing_depends_prev:
            if len(self.__missing_depends_prev) > len(self.missing_dependencies):
                # a dependency has come online
                new_nodes_online = set(self.__missing_depends_prev).symmetric_difference(set(self.missing_dependencies))

                for new in new_nodes_online:
                    self.dependency_online(new, True)

            if len(self.__missing_depends_prev) < len(self.missing_dependencies):
                new_nodes_offline = set(self.missing_dependencies).symmetric_difference(
                    set(self.__missing_depends_prev))

                for new in new_nodes_offline:
                    self.dependency_online(new, False)

            self.__missing_depends_prev = self.missing_dependencies  # update the previous state

        # check if all dependencies have come online
        if self.dependencies_ok and self.__missing_depends_prev_state:
            self.__missing_depends_prev_state = False
            self.all_depends_online()

        elif not self.dependencies_ok and not self.__missing_depends_prev_state:
            self.depends_offline()
            self.__missing_depends_prev_state = True

    def error_callback(self, msg: Error):
        """Callback method for the error messages
        The child class must override this method
        """
        raise NotImplementedError("A subclass must implement this method if it has dependency nodes")
    
    # endregion

    # region METHODS ---------------------------------------------------------------------------------------------------

    def dependency_online(self, name: str, online: bool):
        """Method to notify subclass that a dependency has come online"""
        raise NotImplementedError("A subclass must implement this method if it has dependency nodes")

    def all_depends_online(self):
        """Method to notify subclass that all the dependencies have come online
        The child class must override this method
        """
        raise NotImplementedError("A subclass must implement this method if it has dependency nodes")

    def depends_offline(self):
        """Method to notify subclass that the dependencies have gone offline
        The child class must override this method
        """
        raise NotImplementedError("A subclass must implement this method if it has dependency nodes")

    def publish_error(self, e: UtilsError):
        """Method for publishing error messages to the generated topic"""
        error = Error()
        error.node_name = self.get_name()
        error.error_msg = e.error_msg
        error.error_code = e.error_code

        self.__error_publisher.publish(error)
        
    # endregion

    # region PROPERTIES ------------------------------------------------------------------------------------------------

    @property
    def missing_dependencies(self):
        """Returns the missing nodes

        :returns: a list of all the nodes that are not online
        """
        if not self.__dependencies:
            return []

        missing_depends = list()
        node_names = self.get_node_names()
        for node in self.__dependencies:
            if f"{node}_node" not in node_names:
                missing_depends.append(node)

        return missing_depends

    @property
    def dependencies_ok(self):
        """Returns True if all the dependencies are online, False otherwise"""
        if self.__dependencies is None:
            return True

        node_names = self.get_node_names()
        return all(f'{node_name}_node' in node_names for node_name in self.__dependencies)

    @property
    def dependencies(self):
        """Returns the dependencies of the node"""
        return self.__dependencies
    
    # endregion


class QTROSNode(ROSNode, ABC):
    """ROS Node to use in QT applications"""

    def __init__(self, node_name: str, depends_on: List[str], signals):
        super(QTROSNode, self).__init__(node_name=node_name, depends_on=depends_on)
        self.__signals = signals

    @abstractmethod
    def load_info(self):
        """Load info about the KPI"""

    @abstractmethod
    def load_nodes(self):
        """Load info about the online nodes"""

    @abstractmethod
    def send_control(self, *args, **kwargs):
        """Send messages to the respective control topics"""

    @abstractmethod
    def send_kpi(self, *args, **kwargs):
        """Send KPI messages to the server"""

    @property
    def signals(self):
        """Returns the signals of the object"""
        return self.__signals
