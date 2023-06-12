import os
import logging
from .chat import ChatBot
from .utils import *
from .extract import Extractor

def main():
    setup_logging()
    os.system("clear")

    logging.info("Starting the program")

    announce("Hello", prefix="? Bot: ")
    file_path = prompt_string("Enter the path:")
    chat = ChatBot(file_path)

    while True:
        prompt = prompt_string("Enter your prompt:")
        print("? Bot:")
        chat.send(prompt)
        print("\n")

        should_continue = prompt_confirm("Do you want to continue?")
        if not should_continue:
            break

    announce("Goodbye", prefix="? Bot: ")


def setup_logging():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(message)s")


if __name__ == "__main__":
    main()
