import coloredlogs
import logging

try:
    from rclpy.node import Node
except ImportError as e:
    class Node:
        pass


class Logger:

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
        if self.__parent is not None:
            self.__parent.get_logger().debug(msg)

        else:
            logging.debug(msg)

    def info(self, msg: str):
        if self.__parent is not None:
            self.__parent.get_logger().info(msg)

        else:
            logging.info(msg)

    def warn(self, msg: str):
        if self.__parent is not None:
            self.__parent.get_logger().warn(msg)

        else:
            logging.warning(msg)

    def error(self, msg: str):
        if self.__parent is not None:
            self.__parent.get_logger().error(msg)

        else:
            logging.error(msg)
