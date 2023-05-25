import logging
from openai import ChatCompletion
from .utils import *

def main():
    setup_logging()
    logging.info("Starting the program")

    announce("Hello", prefix="? Bot: ")
    file_path = prompt_string("Enter the file path:")

    while True:
        prompt = prompt_string("Enter your prompt:")
        content = read_file(file_path)

        if content is None:
            logging.error(f"Unable to read file: {file_path}")
            break

        response = generate_response(prompt, content)
        announce(response, prefix="? Bot: ")

        should_continue = prompt_confirm("Do you want to continue? (yes/no)")
        if not should_continue:
            break

    announce("Goodbye", prefix="Bot: ")

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

def generate_response(prompt: str, content: str) -> str:
    try:
        response = ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Respond based on the content from the file and the user prompt."},
                {"role": "user", "content": f"Content:\n\n{content}"},
                {"role": "user", "content": f"Prompt: {prompt}"},
            ],
            temperature=0.1
        )
        return llm_response(response)
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        return "An error occurred while generating the response. Please try again."

def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

if __name__ == "__main__":
    main()