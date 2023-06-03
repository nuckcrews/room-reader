import os
import logging
from .chat import ChatBot
from .utils import *

def main():
    setup_logging()
    os.system("clear")

    logging.info("Starting the program")

    announce("Hello", prefix="? Excel Wizard: ")
    file_path = "./example/SaleData.xlsx"
    # file_path = prompt_string("Enter path to excel file:")
    chat = ChatBot(file_path)

    while True:
        prompt = prompt_string("Enter your prompt:")
        print("? Excel Wizard:")
        chat.send(prompt)
        print("\n")

        should_continue = prompt_confirm("Do you want to continue?")
        if not should_continue:
            break

    announce("Goodbye", prefix="? Excel Wizard: ")


def setup_logging():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(message)s")


if __name__ == "__main__":
    main()