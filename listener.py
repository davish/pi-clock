#!/usr/bin/env python3

from gpiozero import Button
from signal import pause
from subprocess import check_call

from Adafruit_Thermal import *

from common import register_callback, setup_gpio, is_sleeping, absolute_path_of
from tick import tick


printer = Adafruit_Thermal("/dev/serial0", 9600, timeout=5)


counter = 0

TICK_PY = absolute_path_of("tick.py")

def handler(x):
    if is_sleeping():
        print("brighten for a minute.")
        # check_call([TICK_PY, "--bright"])
        tick(True)
    else:
        print("not sleeping. noop for now.")

setup_gpio()
register_callback(handler)
pause()
