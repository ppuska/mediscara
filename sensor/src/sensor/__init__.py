"""Init module for the sensor package"""
import coloredlogs

__version__ = "0.0.1"

LOG_LEVEL = "DEBUG"

coloredlogs.install(level=LOG_LEVEL,
                    fmt="%(asctime)s,%(msecs)03d %(hostname)s %(name)s[%(process)d] %(levelname)s %(message)s"
                    )
