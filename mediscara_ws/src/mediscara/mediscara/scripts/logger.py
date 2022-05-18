"""Module for managing ROS-based and plain logging"""
import logging

import coloredlogs

try:
    from rclpy.node import Node
except ImportError as e:

    class Node:
        """Dummy import class"""

        pass


class Logger:
    """Class for managing logging messages"""

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR

    def __init__(self, parent, tag: str = "", level: int = logging.INFO):
        coloredlogs.install(level)
        self.__parent = parent
        # noinspection PyBroadException
        try:
            self.__parent.get_logger()
        except AttributeError:
            self.__parent = None
        self.__tag = tag

    def debug(self, msg: str):
        """Print debug messages"""
        if self.__parent is not None:
            self.__parent.get_logger().debug(f"{self.__tag} {msg}")

        else:
            logging.debug("%s %s", self.__tag, msg)

    def info(self, msg: str):
        """Prints info messages"""
        if self.__parent is not None:
            self.__parent.get_logger().info(f"{self.__tag} {msg}")

        else:
            logging.info("%s %s", self.__tag, msg)

    def warn(self, msg: str):
        """Prints warning messages"""
        if self.__parent is not None:
            self.__parent.get_logger().warn(f"{self.__tag} {msg}")

        else:
            logging.warning("%s %s", self.__tag, msg)

    def error(self, msg: str):
        """Prints error messages"""
        if self.__parent is not None:
            self.__parent.get_logger().error(f"{self.__tag} {msg}")

        else:
            logging.error("%s %s", self.__tag, msg)
