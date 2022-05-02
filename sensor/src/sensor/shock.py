"""Module for the shock sensor"""

from typing import Callable
import RPi.GPIO as gpio

def initialize(pin_shock: int, callback: Callable[[int], None]):
    """Initializes the GPIO pin to receive the interrupt

    Args:
        callback (Callable[None, [None]]): Callback function when the sensor sends the signal
    """
    gpio.setmode(gpio.BCM)
    gpio.setup(pin_shock, gpio.IN)

    gpio.add_event_detect(pin_shock, gpio.RISING, callback=callback, bouncetime=100)