#!/usr/bin/env python3

from datetime import datetime
import board
from adafruit_ht16k33.segments import Seg7x4

def main():
    i2c = board.I2C()
    display = Seg7x4(i2c)

    display.brightness = 0.5
    now = datetime.now()
    current_time = now.strftime("%I:%M")
    if current_time.startswith("0"):
        current_time = " " + current_time[1:]
    display.print(current_time)

if __name__ == "__main__":
    main()
