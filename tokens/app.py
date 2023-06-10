import os
import logging
from .utils import *
from .extract import Extractor


def main():
    setup_logging()
    os.system("clear")

    logging.info("Starting the program")

    announce("Token Counter")

    while True:
        file_path = prompt_string("Enter the path:")

        extractor = Extractor(file_path)
        file = extractor.extract()
        print(file.content)
        announce(file.path, prefix="? Bot: ")

        announce(num_tokens(file.content), prefix="Tokens: ")

        should_continue = prompt_confirm("Do you want to continue?")
        if not should_continue:
            break

    announce("Goodbye", prefix="? Bot: ")


def setup_logging():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(message)s")


if __name__ == "__main__":
    main()
