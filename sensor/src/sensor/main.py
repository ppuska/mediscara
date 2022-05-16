import sys
from time import sleep
import argparse

from . import __version__
from .sensor import Sensor
from . import config

SERVER_ADDRESS = "server_address"
UPDATE_INTERVAL = "update_interval"

def parse_args(args):
    """Parses the command line arguments"""
    arg_parser = argparse.ArgumentParser(
        description="""This is a command line interface to the sensor node
        in the MediScara project"""
        )

    arg_parser.add_argument('--version', action='version', version=f"sensor: {__version__}")
    arg_parser.add_argument('-s', '--server',
                            dest=SERVER_ADDRESS,
                            type=str,
                            default=config.SERVER_ADDRESS,
                            help="The address of the server hosting the OCB"
                            )
    arg_parser.add_argument('-i', '--interval',
                            dest=UPDATE_INTERVAL,
                            type=int,
                            default=config.UPDATE_INTERVAL,
                            help="The sensor's update interval in seconds"
                            )

    return arg_parser.parse_args(args=args)

def main():
    opts = vars(parse_args(sys.argv[1:]))
    server_address = opts.get(SERVER_ADDRESS)
    update_interval = opts.get(UPDATE_INTERVAL)

    sensor = Sensor(14, server_address)

    try:
        while True:
            print(sensor.update())
            sleep(update_interval)

    except KeyboardInterrupt:
        print("\nExiting")


if __name__ == "__main__":
    main()
