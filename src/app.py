import os
import logging
import time
from openai import ChatCompletion
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

def generate_response(prompt: str, content: str):
    try:
        response = ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Respond based on the content from the file and the user prompt."},
                {"role": "user", "content": f"Content:\n\n{content}"},
                {"role": "user", "content": f"Prompt: {prompt}"},
            ],
            temperature=0.1,
            stream=True
        )

        stripped = False
        for event in response:
            delta = event.get('choices')[0].get('delta')
            event_text = None
            if delta:
                event_text = delta.get('content')

            if not event_text:
                continue

            if not stripped:
                event_text = event_text.strip()
                stripped = True

            stream(event_text)

    except Exception as e:
        logging.error(f"Error generating response: {e}")
        return "An error occurred while generating the response. Please try again."

def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

if __name__ == "__main__":
    main()