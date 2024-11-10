import os
from dotenv import load_dotenv
from playsound import playsound
from src.bot_sipd import SIPDBot

load_dotenv()


def play_notification(audio_type=1):
    audio_path = {
        1: "assets/audio/mixkit-happy-bells-notification-937.wav",
        2: "assets/audio/mixkit-software-interface-start-2574.wav",
        3: "assets/audio/mixkit-software-interface-back-2575.wav",
        4: "assets/audio/mixkit-correct-answer-tone-2870.wav",
    }

    try:
        playsound(audio_path[audio_type])
    except FileNotFoundError:
        print(f"Audio error: The audio file '{audio_path[audio_type]}' was not found.")
    except PermissionError:
        print(f"Audio error: Permission denied accessing '{audio_path[audio_type]}'.")
    except KeyError:
        print(f"Audio error: Audio not found for type {audio_type}")
    except Exception as e:
        print(f"Audio error: {e}")


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
