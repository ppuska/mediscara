try:
    from rclpy.node import Node
except ImportError as e:
    class Node:
        pass


class Logger:
    DEBUG = 3
    INFO = 2
    WARN = 1
    ERROR = 0

    LOG_LEVEL = DEBUG

    def __init__(self, parent: Node or None, tag: str = ""):
        self.__parent = parent
        # noinspection PyBroadException
        try:
            self.__parent.get_logger()
        except Exception:
            self.__parent = None
        self.__tag = tag

    def debug(self, msg: str):
        if self.__parent is not None:
            self.__parent.get_logger().debug(msg)

        else:
            if Logger.LOG_LEVEL >= Logger.DEBUG:
                print(f'{self.__tag} DEBUG\t', msg)

    def info(self, msg: str):
        if self.__parent is not None:
            self.__parent.get_logger().info(msg)

        else:
            if Logger.LOG_LEVEL >= Logger.INFO:
                print(f'{self.__tag} INFO\t', msg)

    def warn(self, msg: str):
        if self.__parent is not None:
            self.__parent.get_logger().warn(msg)

        else:
            if Logger.LOG_LEVEL >= Logger.WARN:
                print(f'{self.__tag} WARN\t', msg)

    def error(self, msg: str):
        if self.__parent is not None:
            self.__parent.get_logger().error(msg)

        else:
            if Logger.LOG_LEVEL >= Logger.ERROR:
                print(f'{self.__tag} ERROR\t', msg)
