from datetime import datetime

fmt = "%I:%M %p"

def to_string(d):
    return d.strftime(fmt)

def from_string(s):
    return datetime.strptime(s, fmt).time()
