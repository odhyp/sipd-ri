import os
import time
import winsound

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()


def play_notification():
    sound_path = "assets/notification.wav"
    try:
        winsound.PlaySound(sound_path, winsound.SND_FILENAME)
    except KeyboardInterrupt:
        pass


class SIPDBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = None
        self.context = None
        self.page = None

    def initialize_browser(self):
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(
            headless=False, args=["--start-maximized"]
        )
        self.context = self.browser.new_context(no_viewport=True)
        self.page = self.context.new_page()


def main():
    username = os.getenv("SIPD_USERNAME")
    password = os.getenv("SIPD_PASSWORD")


if __name__ == "__main__":
    main()
