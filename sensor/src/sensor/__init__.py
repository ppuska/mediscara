"""Init module for the sensor package"""
import coloredlogs

LOG_LEVEL = "INFO"

coloredlogs.install(level=LOG_LEVEL,
                    fmt="%(asctime)s,%(msecs)03d %(hostname)s %(name)s[%(process)d] %(levelname)s %(message)s"
                    )
