#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from PIL import Image
import io

from Adafruit_Thermal import *

printer = Adafruit_Thermal("/dev/serial0", 9600, timeout=5)

def get_xkcd():
    r = requests.get('https://xkcd.com/atom.xml')
    xml_soup = BeautifulSoup(r.text)
    latest = xml_soup.find_all("entry")[0]
    comic = BeautifulSoup(latest.find("summary").text).find("img")
    return {"url": comic.get("src"), "alt": comic.get("alt"), "title": latest.find("title").text}

if __name__ == "__main__":
    comic = get_xkcd()
    r = requests.get(comic["url"], stream=True)
    if r.status_code == 200:
        img = Image.open(io.BytesIO(r.content))
        printer.printImage(img, True)
        printer.feed(3)
