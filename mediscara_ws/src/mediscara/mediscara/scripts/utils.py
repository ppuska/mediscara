"""Module for utility-related code"""
from dataclasses import dataclass

from interfaces.msg import Error


@dataclass
class ErrorClass:
    """Dataclass for storing error codes and their content"""

    error_code: int
    error_msg: str

    @classmethod
    def from_error_msg(cls, e_msg: Error):
        """Generates a class instance from a ROS Error message"""
        return cls(error_msg=e_msg.error_msg, error_code=e_msg.error_code)
