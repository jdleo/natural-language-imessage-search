import platform
from dotenv import load_dotenv
from os import getenv, path
from ui import create_ui

load_dotenv()


def check_compatibility():
    if not platform.system() == "Darwin":
        exit("This app is only compatible with macOS - exiting.")

    if not getenv("OPENROUTER_API_KEY"):
        exit(
            "Please set the OPENROUTER_API_KEY environment variable in an .env file in the root of the project - exiting."
        )

    if not path.exists(path.expanduser("~/Library/Messages/chat.db")):
        exit(
            "Please ensure that your iMessage history is stored in ~/Library/Messages/chat.db - exiting."
        )


if __name__ == "__main__":
    check_compatibility()
    demo = create_ui()
    demo.launch()
