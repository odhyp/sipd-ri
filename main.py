import os
from dotenv import load_dotenv
from src.bot_sipd import SIPDBot

load_dotenv()


def main():
    username = os.getenv("SIPD_USERNAME")
    password = os.getenv("SIPD_PASSWORD")

    bot = SIPDBot(username=username, password=password)
    bot.start_browser()

    bot.download_realisasi(1)
    bot.sample()

    bot.close_browser()


if __name__ == "__main__":
    main()
