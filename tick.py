#!/usr/bin/env python3

from datetime import datetime
import json

import board
from adafruit_ht16k33.segments import Seg7x4

from common import from_string

SLEEP_SETTINGS = "settings/sleep.json"

def get_time_string(d):
    time_string = d.strftime("%I:%M")
    if time_string.startswith("0"):
        time_string = " " + time_string[1:]
    return time_string

def main():
    i2c = board.I2C()
    display = Seg7x4(i2c)

    display.brightness = 0.5

    now = datetime.now()

    with open(SLEEP_SETTINGS, "r") as f:
        sleep_settings = json.load(f)

    nowt = now.time()

    if from_string(json["begin"]) < nowt or nowt < from_string(json["end"]):
        display.fill(0)
    else:
        display.print(current_time)

if __name__ == "__main__":
    main()
