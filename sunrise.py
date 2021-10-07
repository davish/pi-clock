#!/usr/bin/env python3

import requests
import datetime
import os
from time import sleep

from common import absolute_path_of, from_string
import json


SETTINGS = absolute_path_of("settings.json")

BRIGHTNESS_MAX = 255
BRIGHTNESS_MIN = 0

COLOR_MAX = 454
COLOR_MIN = 400

SUNRISE_DURATION_MINS = 30


KEY = "B679503A5B"  # TODO: move the key out of the git repo
URL = f"http://solaris.local:80/api/{KEY}/lights/2/state"

def time_diff(a, b):
    return datetime.datetime.combine(datetime.datetime.min, a) - datetime.datetime.combine(datetime.datetime.min, b)

def progress(start, current, end):
    print(start, current, end)
    print(time_diff(current, end).seconds)
    time_after_end = time_diff(current, end)
    if current < start:
        return 0.0
    if time_after_end.days >= 0 and time_after_end.seconds > (60 * 60):
        return 0.0

    total = time_diff(end, start)
    diff = time_diff(current, start)

    return max(min(diff.seconds / total.seconds, 1.0), 0.0)

def update_light(on, brightness=None, color=None):
    payload = {"on": on} 
    if brightness is not None:
        payload["bri"] = round((BRIGHTNESS_MAX - BRIGHTNESS_MIN) * brightness + BRIGHTNESS_MIN)
    if color is not None:
        payload["ct"] = round(COLOR_MAX - (COLOR_MAX - COLOR_MIN) * color)

    r = requests.put(URL, json=payload)
    sleep(2.0)
    r = requests.put(URL, json=payload)  # for some reason need to double up on requests.



def sunrise():
    with open(SETTINGS, "r") as f:
        sunrise_finish = from_string(json.load(f)["sunrise"])
    sunrise_start = (datetime.datetime.combine(datetime.datetime.min, sunrise_finish) - datetime.timedelta(minutes=SUNRISE_DURATION_MINS)).time()
    current_time = datetime.datetime.now().time()

    percent_progress = progress(sunrise_start, current_time, sunrise_finish)
    update_light(percent_progress > 0, percent_progress, percent_progress)

if __name__ == "__main__":
    if KEY is None:
        exit(1)
    sunrise()
