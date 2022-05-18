"""Init module for the manager package"""
import coloredlogs

__version__ = "0.0.0"

coloredlogs.install(
    level="DEBUG",
    fmt="%(asctime)s,%(msecs)03d %(hostname)s %(name)s[%(process)d] %(levelname)s %(message)s",
)
