#!/usr/bin/env python3

from datetime import datetime
import json
import argparse

import board
from adafruit_ht16k33.segments import Seg7x4

from common import from_string, absolute_path_of, is_sleeping


def get_time_string(d):
    time_string = d.strftime("%I:%M")
    if time_string.startswith("0"):
        time_string = " " + time_string[1:]
    return time_string


def tick(force_bright=False):
    i2c = board.I2C()
    display = Seg7x4(i2c)
    display.brightness = 0.5

    now = datetime.now()

    if is_sleeping() and not force_bright:
        print("sleep mode, turning off display...")
        display.fill(0)
    else:
        current_time = get_time_string(now)
        display.print(current_time)

def setup_parser(parser):
    parser.add_argument("--bright", action="store_true")


def main(args):
    tick(args.bright)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    setup_parser(parser)
    args = parser.parse_args()
    main(args)
