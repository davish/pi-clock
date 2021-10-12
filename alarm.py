#!/usr/bin/env python3

import json
from datetime import datetime
import requests
from pygame import mixer
from time import sleep
from signal import pause

from common import to_string, from_string, absolute_path_of, setup_gpio, register_callback, clear_callback

import podcast

SETTINGS = absolute_path_of("settings.json")
LAST_ALARM = absolute_path_of("data/LAST_ALARM")
RING = absolute_path_of("ring.mp3")

KEY = "B679503A5B"  # TODO: move the key out of the git repo
URL = f"http://solaris.local:80/api/{KEY}/lights/2/state"


been_pressed = False

def play():
    mixer.music.play()
    while mixer.music.get_busy() and not been_pressed:
        sleep(0.1)

def handler(x):
    global been_pressed
    been_pressed = True

def sound_alarm():
    mixer.init()
    mixer.music.load(RING)
    while not been_pressed:
        play()
        sleep(0.5)

def get_alarms():
    with open(SETTINGS, "r") as alarmfile:
        alarms = json.load(alarmfile)["alarms"]
    return [from_string(k) for k, v in alarms.items() if v]

def time_diff(a, b):
    return (a.hour - b.hour) * 60 + (a.minute - b.minute)

def get_next_alarm(alarms):
    now = datetime.now().time()
    try:
        next_alarm = sorted([a for a in alarms if now > a ], key=lambda t: time_diff(now, t))[0]
        return next_alarm
    except IndexError:
        return None

def should_sound_alarm(alarm_time):
    try:
        with open(LAST_ALARM, "r") as f:
            last_alarm = datetime.fromisoformat(f.read())
    except (ValueError, FileNotFoundError):
        last_alarm = datetime(1970, 1, 1)
    now = datetime.now().time()
    if last_alarm.date() < datetime.now().date() and alarm_time == now:
        return True, True

    if alarm_time == now:
        # If we sounded an earlier alarm, then sound this one.
        return True, False

    return False, False

def main():
    setup_gpio()
    alarms = get_alarms()
    next_alarm = get_next_alarm(alarms)
    if next_alarm is None:
        return
    should_sound, first_alarm = should_sound_alarm(next_alarm)
    if should_sound:
        register_callback(handler)
        with open(LAST_ALARM, "w") as f:
            f.write(datetime.now().isoformat())

        payload = {
            "on": True,
            "bri": 40,
            "ct": 450

        }
        r = requests.put(URL, json=payload)
        sleep(2.0)
        r = requests.put(URL, json=payload)  # for some reason need to double up on requests.
        sound_alarm()
        clear_callback()
        register_callback(lambda x: exit(0))
        podcast.play()



if __name__ == "__main__":
    main()
