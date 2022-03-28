import logging
import socket
import threading
from functools import wraps
from typing import Callable, Tuple

from .logger import Logger
from .thread_manager import WorkerThread


class Decorator:
    @staticmethod
    def socket_check(func):
        """Wraps a try...except case around the function to except socket exceptions"""

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)

                return result

            except OSError as e:
                logging.error(f"Socket error in {func.__name__}: {e}")

        return wrapper


class SocketManager:
    """Class for implementing socket communication as a client"""

    MAX_RETRIES = 5

    def __init__(self,
                 parent,
                 is_server: bool,
                 host: str = 'localhost',
                 port: int = 65432,
                 blocking: bool = True,
                 received_callback: Callable[[bool, str], None] = None,
                 connected_callback: Callable[[str], None] = None
                 ):
        """
        Constructor method

        Creates the Socket node and configures it to be a server or a client and to have blocking or non-blocking calls

        If the class is in server mode, the bind_and_accept method should be used, if it is in client mode, the connect
        method should be used

        :param parent: the parent node of the class
        :param is_server: True if the socket is a socket server, False if it is a client
        :param host: the IP address of the socket communication
        :param port: the port of the communication
        :param blocking: if False, the blocking methods will be run in a separate thread
        :param received_callback: callback method for non-blocking receive calls
        :param connected_callback: callback method for non-blocking connect calls
        """
        super(SocketManager, self).__init__()
        self.__is_server = is_server
        self.__host = host
        self.__port = port
        self.__blocking = blocking
        if not self.__blocking:
            if received_callback is None or connected_callback is None:
                raise Exception("When in non-blocking mode, callbacks must not be None")

        self.__received_callback = received_callback
        self.__connected_callback = connected_callback

        if self.__is_server:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__client_socket = None

        else:
            self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket = None

        self.__socket_connected = False

        self.__logger = Logger(parent=parent)

        self.__initial_connect = True  # variable to only display connection message once

        self.__connect_thread = None
        self.__listen_thread = None

    def connect(self) -> Tuple[bool, str] or None:
        """Connects to the selected port as a client

        :returns: a tuple of the operation success and message, or None if the method ran async
        """
        if self.__initial_connect:
            self.__logger.info(f"Connecting to '{self.__host}:{self.__port}'")
            self.__initial_connect = False

        if self.__blocking:  # check if blocking mode is enabled

            if self.__is_server:  # check if the socket is a server
                raise Exception(f"Server cannot connect to socket, use '{self.bind_and_accept.__name__}' method")

            else:
                return self._socket_connect(None)

        else:
            self.__connect_thread = WorkerThread(  # create socket thread
                worker_function=self._socket_connect,
                result_callback=self._connected_callback_internal,
                loop=True
            )
            self.__connect_thread.start()

    def bind_and_accept(self) -> Tuple[bool, str] or None:
        """Binds and accepts a socket connection

        :returns: a tuple of the operation success and message, or None if the method ran async
        """
        self.__logger.info(f"Binding to '{self.__port}'")
        if self.__blocking:
            if not self.__is_server:
                raise Exception(f"Client cannot bind to socket, use '{self.connect.__name__}' method")

            success, message = self._bind_and_accept(threading.Lock())
            if not success:
                self.__logger.warn(message)

            else:
                self.__logger.info(message)

            return success, message

        else:
            if not self.__is_server:
                raise Exception(f"Client cannot bind to socket, use '{self.connect.__name__}' method")

            self.__connect_thread = WorkerThread(
                worker_function=self._bind_and_accept,
                result_callback=self._bound_callback_internal,
                loop=False
            )
            self.__connect_thread.start()

    @Decorator.socket_check
    def receive(self):
        """Receives message from the socket

        Blocking call
        """
        if not self.__blocking:
            raise Warning(f"In non-blocking mode use the '{self.start_receive.__name__}' method")
        return self.__socket.recv(1024).decode('utf-8')

    @Decorator.socket_check
    def send(self, msg: str):
        self.__client_socket.sendall(msg.encode('utf-8'))

    def start_receive(self):
        """Starts the receiver thread that listens to incoming communication on the socket

        Cannot be run in blocking mode
        """
        self.__logger.info("Started receiving...")

        if self.__blocking:
            raise Exception("In blocking mode cannot start listening threads")

        self.__listen_thread = WorkerThread(
            worker_function=self._listen,
            result_callback=self._received_callback_internal,
            loop=True
        )
        self.__listen_thread.start()

    def close(self):
        if self.__client_socket is not None:
            assert isinstance(self.__client_socket, socket.socket)
            self.__client_socket.close()

        if self.__socket is not None:
            assert isinstance(self.__socket, socket.socket)
            self.__socket.close()

    def _socket_connect(self, _):
        """Private method for connecting to the socket
        """
        error_msg = ""
        for i in range(self.MAX_RETRIES):
            try:
                self.__client_socket.connect((self.__host, self.__port))

            except ConnectionRefusedError:
                error_msg = "Connection refused by host"

            except ConnectionError:
                error_msg = "Connection error"

            except socket.timeout:
                error_msg = "Socket timed out"

            except TimeoutError:
                error_msg = "Socket timed out"

            else:
                self.__socket_connected = True
                return True, "Socket connected"

        return False, error_msg

    def _connected_callback_internal(self, success, message):
        """Internal callback method for connection results
        Calls the callback method of the superclass
        """
        if success:
            self.__logger.info(message)
            self.__connect_thread.stop()
            self.__connected_callback(message)

        else:
            self.__logger.warn(message)

    def _bound_callback_internal(self, success, message):
        """Internal callback method for binding attempt results
        Calls the callback method of the superclass
        """
        if success:
            self.__logger.info(message)
            self.__connect_thread.stop()
            self.__connected_callback(message)

        else:
            self.__logger.warn(message)

    def _received_callback_internal(self, success, message):
        """Internal callback method for received communication results
        Calls the callback method of the superclass
        """
        if success:
            if message == "":
                """ Empty message as a client means disconnected server"""
                self.__logger.warn("Socket disconnected")
                self.__listen_thread.stop()  # stop the listen thread
                self.__client_socket.close()
                self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.__initial_connect = True
                message = "Empty message"
                success = False
                self.__socket_connected = False

        else:
            if message == "Connection reset":
                return

            self.__logger.warn(message)

        self.__received_callback(success, message)

    def _bind_and_accept(self, lock: threading.Lock):
        """Private method for binding and accepting a socket for socket server communication"""
        error_msg = ""
        for i in range(self.MAX_RETRIES):
            try:
                self.__socket.bind((self.__host, self.__port))
                self.__socket.listen()
                conn, address = self.__socket.accept()
                lock.acquire()
                self.__client_socket = conn
                lock.release()

            except ConnectionRefusedError:
                error_msg = "Connection refused by host"

            except ConnectionError:
                error_msg = "Connection error"

            except socket.timeout:
                error_msg = "Socket timed out"

            else:
                self.__socket_connected = True
                return True, 'Socket bound and listening...'

        return False, error_msg

    def _listen(self, _):
        """Private method for listening to the communication"""
        try:
            response = self.__client_socket.recv(1024).decode('utf-8')
            return True, response

        except ConnectionRefusedError:
            return False, "Connection refused"

        except ConnectionAbortedError:
            return False, "Connection aborted"

        except ConnectionResetError:
            return False, "Connection reset"


if __name__ == '__main__':
    import time


    def rec_callback(success, message):
        if not success:
            server.connect()


    def connect_cb(success, _):
        if success:
            server.start_receive()
        else:
            server.connect()


    server = SocketManager(parent=None,
                           host='localhost',
                           port=65432,
                           connected_callback=connect_cb,
                           received_callback=rec_callback,
                           is_server=False,
                           blocking=False
                           )

    try:
        server.connect()

        count = 0
        while True:
            # print(f"\rCycle: {count}", end='')
            time.sleep(1)
            count += 1

    except KeyboardInterrupt:
        print("Stopping")
