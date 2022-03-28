from dataclasses import dataclass

from interfaces.msg import Error


@dataclass
class ErrorClass:
    error_code: int
    error_msg: str

    @classmethod
    def from_error_msg(cls, e: Error):
        return cls(error_msg=e.error_msg, error_code=e.error_code)
