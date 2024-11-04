import os
import time
import winsound

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()


def play_notification():
    sound_path = "assets/notification.wav"
    winsound.PlaySound(sound_path, winsound.SND_FILENAME)


def main():
    username = os.getenv("SIPD_USERNAME")
    password = os.getenv("SIPD_PASSWORD")

    play_notification(5)


if __name__ == "__main__":
    main()
