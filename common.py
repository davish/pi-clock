import RPi.GPIO as GPIO
from datetime import datetime
import os
import json


fmt = "%I:%M %p"


def to_string(d):
    return d.strftime(fmt)


def from_string(s):
    return datetime.strptime(s, fmt).time()


def absolute_path_of(fname):
    return os.path.dirname(os.path.realpath(__file__)) + f"/{fname}"


def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def register_callback(cb, port=5):
    GPIO.add_event_detect(port, GPIO.RISING, callback=cb, bouncetime=500)


def clear_callback(port=5):
    GPIO.remove_event_detect(port)


SETTINGS = absolute_path_of("settings.json")


def is_sleeping():
    with open(SETTINGS, "r") as f:
        sleep_settings = json.load(f)["sleep"]
    now = datetime.now().time()

    return from_string(sleep_settings["begin"]) < now or now < from_string(sleep_settings["end"])
