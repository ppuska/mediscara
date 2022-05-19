"""Module for serial communication with devices"""
import sys
from typing import Callable

import serial
from mediscara.scripts.logger import Logger
from mediscara.scripts.thread_manager import WorkerThread


class SerialManager:
    """Class for managing serial communication"""

    __PORT_WIN = "COM10"
    __PORT_LINUX = None  # todo

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        parent,
        blocking: bool,
        baud: int = 9600,
        parity=serial.PARITY_NONE,
        data_bits=serial.EIGHTBITS,
        read_callback: Callable[[str], None] = None,
    ):

        self.__blocking = blocking
        self.__logger = Logger(parent=parent)
        self.__serial_port = serial.Serial(port=None, baudrate=baud, parity=parity, bytesize=data_bits)
        self.__read_callback = read_callback

        # get the system platform
        if sys.platform.startswith("win"):  # windows platform, debug mode
            self.__serial_port.port = self.__PORT_WIN

        elif sys.platform.startswith("linux") or sys.platform.startswith("cygwin"):  # linux
            self.__serial_port.port = self.__PORT_LINUX

        else:
            raise EnvironmentError("Unsupported platform")

        if not self.__blocking and self.__read_callback is None:
            raise AssertionError("In non-blocking mode, the read_callback cannot be null")

        self.__read_thread = None

    def open(self) -> bool:
        """Opens the serial port
        :returns: True if successful, else False
        """
        try:
            self.__serial_port.open()
            return True

        except serial.SerialException:
            self.__logger.warn("Unable to open serial port")
            return False

    def close(self) -> bool:
        """Closes the serial port
        :returns: True if successful, False if an error occurred"""
        try:
            self.__serial_port.close()
            return True

        except serial.SerialException:
            self.__logger.warn("Unable to close serial port")
            return False

    def send(self, message: str):
        """Sends the message via the serial communication"""
        try:
            self.__serial_port.write(message.encode("utf-8"))
        except serial.PortNotOpenError:
            self.__logger.warn("Port not open, cannot send data")

    def read(self):
        """Reads the incoming stream until the terminator character"""
        if self.__serial_port.is_open:
            return self._read(None)

        return None

    def start_read(self):
        """Starts the reading thread"""
        if self.__blocking:
            raise Warning("Cannot start non-blocking read thread in blocking mode")

        if not self.__serial_port.is_open:
            self.__logger.warn("Port not open, cannot start read thread")
            return

        self.__logger.info("Staring read thread")
        self.__read_thread = WorkerThread(
            worker_function=self._read, result_callback=self.__read_callback_internal, loop=True
        )
        self.__read_thread.start()

    def _read(self, _):
        try:
            response = self.__serial_port.read_until().decode("utf-8")  # read until the terminator, and decode to str
            return True, response

        except serial.PortNotOpenError:
            return False, "Serial port not open, cannot read"

        except serial.SerialException:
            return False, "Serial error"

    def __read_callback_internal(self, success: bool, message: str):
        print("read callback internal | success: ", success)
        if not success:
            self.close()
            self.open()

        else:
            self.__read_callback(message)
