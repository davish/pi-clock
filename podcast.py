#!/usr/bin/env python3

import requests
import argparse
from time import sleep

from bs4 import BeautifulSoup

from common import absolute_path_of

PODCAST = absolute_path_of("data/podcast.mp3")

def get():
    r = requests.get('https://feeds.npr.org/510318/podcast.xml')
    soup = BeautifulSoup(r.text)

    podcast_url = soup.find_all("enclosure")[0].get("url")

    podcast = requests.get(podcast_url)

    with open(PODCAST, "wb") as fd:
        for chunk in podcast.iter_content(chunk_size=128):
            fd.write(chunk)

def play():
    from pygame import mixer
    mixer.init()
    mixer.music.load(PODCAST)
    mixer.music.play()
    while mixer.music.get_busy():
        sleep(0.1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd")
    args = parser.parse_args()
    if args.cmd == "play":
        play()
    elif args.cmd == "get":
        get()

if __name__ == "__main__":
    main()
