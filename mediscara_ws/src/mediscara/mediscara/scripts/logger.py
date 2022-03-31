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
            self.__parent.get_logger().debug(f"{self.__tag} {msg}")

        else:
            logging.debug(f"{self.__tag} {msg}")

    def info(self, msg: str):
        if self.__parent is not None:
            self.__parent.get_logger().info(f"{self.__tag} {msg}")

        else:
            logging.info(f"{self.__tag} {msg}")

    def warn(self, msg: str):
        if self.__parent is not None:
            self.__parent.get_logger().warn(f"{self.__tag} {msg}")

        else:
            logging.warning(f"{self.__tag} {msg}")

    def error(self, msg: str):
        if self.__parent is not None:
            self.__parent.get_logger().error(f"{self.__tag} {msg}")

        else:
            logging.error(f"{self.__tag} {msg}")
