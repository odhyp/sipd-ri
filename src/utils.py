import os
from pathlib import Path
from playsound import playsound


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
        print(f"Audio error: Audio not found for type {audio_type}.")
    except RuntimeError:
        print(f"Audio error: Audio playback error.")
    except Exception as e:
        print(f"Audio error: {e}.")


def get_month_name(index):
    month_list = [
        "Januari",
        "Februari",
        "Maret",
        "April",
        "Mei",
        "Juni",
        "Juli",
        "Agustus",
        "September",
        "Oktober",
        "November",
        "Desember",
    ]
    return month_list[index - 1]


class PathHelper:

    @staticmethod
    def get_download_path() -> str:
        pass

    @staticmethod
    def get_root_path() -> str:
        root_path = Path(os.getcwd())
        return str(root_path)

    @staticmethod
    def get_output_path(output_dir: str, file_name: str) -> str:
        output_path = Path("output", output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        output_path = Path(output_path, file_name)
        return str(output_path)
