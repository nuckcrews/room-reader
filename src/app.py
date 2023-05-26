import os
import logging
import time
from openai import ChatCompletion
from .utils import *

def main():
    setup_logging()
    logging.info("Starting the program")

    announce("Hello", prefix="? Bot: ")
    file_path = prompt_string("Enter the path:")
    if is_directory(file_path):
        content = get_directory_content(file_path)
    else:
        content = read_file(file_path)

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

def is_directory(path: str) -> bool:
    return os.path.isdir(path)

# Get the content of each file in a directory and return a list
def get_directory_content(path: str) -> str:
    file_contents = []
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
                file_contents.append(content)
    return file_contents

def read_file(path: str) -> str:
    try:
        with open(path, "r") as f:
            return f.read(10000)
    except FileNotFoundError:
        logging.error(f"File not found: {path}")
        return None
    except Exception as e:
        logging.error(f"Error reading file: {path}, {e}")
        return None

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