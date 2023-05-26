import os
import logging
import time
from openai import ChatCompletion
from .generate import generate_response
from .extract import Extractor
from .utils import *

def main():
    setup_logging()
    logging.info("Starting the program")

    announce("Hello", prefix="? Bot: ")
    file_path = prompt_string("Enter the path:")
    content = Extractor(file_path).extract()

    while True:
        prompt = prompt_string("Enter your prompt:")

        if content is None:
            logging.error(f"Unable to read file: {file_path}")
            break

        print("? Bot:")
        generate_response(prompt, content)
        print("\n")

        should_continue = prompt_confirm("Do you want to continue? (yes/no)")
        if not should_continue:
            break

    announce("Goodbye", prefix="Bot: ")

def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

if __name__ == "__main__":
    main()