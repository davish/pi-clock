from datetime import datetime

fmt = "%I:%M %p"

def to_string(d):
    return d.strftime(fmt)

def from_string(s):
    return datetime.strptime(s, fmt).time()

def set_data(fname, s):
    with open(fname, "w") as f:
        f.write(s)

def get_data(fname, parse=lambda x: x, default=None):
    try:
        with open(fname, "r") as f:
            return parse(f.read())
    except FileNotFoundError, Exception:
        return default
