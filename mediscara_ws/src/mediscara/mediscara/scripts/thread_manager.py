"""This is a module containing the thread management code"""

import threading
from typing import Callable, Tuple


class WorkerThread(threading.Thread):
    """Worker thread class for managing long-running processes on a separate daemon thread"""

    lock = threading.Lock()

    def __init__(
        self,
        worker_function: Callable[[threading.Lock], Tuple[bool, str]],
        result_callback: Callable[[bool, str], None],
        loop: bool,
    ):
        """
        Constructor method
            :param worker_function:
                the long-running function, should take one argument, which is a threading lock
            :param result_callback:
                callback function for the result, which is a tuple of a bool indicating success, and a
                result string
            :param loop:
                whether the worker function should run in an indefinite loop
        """
        self.__worker = worker_function
        self.__result_callback = result_callback
        self.__loop = loop
        self.__is_running = False

        super().__init__(daemon=True)

    def __del__(self):
        if self.__loop:
            self.stop()
        while self.__is_running:
            pass

    def run(self) -> None:
        self.__is_running = True

        if not self.__loop:
            success, msg = self.__worker(self.lock)
            with self.lock:
                self.__result_callback(success, msg)

        else:
            while True:
                with self.lock:
                    if not self.__is_running:
                        return

                success, msg = self.__worker(self.lock)

                with self.lock:
                    self.__result_callback(success, msg)

        self.__is_running = False

    def stop(self):
        """Attempts to stop a looping thread from re-executing"""
        if not self.__loop:
            raise Warning("Cannot stop a non-looping thread")

        self.__is_running = False

    @property
    def running(self):
        """Returns wether the thread is running or not"""
        return self.__is_running

    @property
    def looping(self):
        """Returns wether the thread is set to loop or not"""
        return self.__loop
