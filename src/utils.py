import sys
import json
import tiktoken
import logging
from PyInquirer import prompt

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

__all__ = [
    "announce",
    "stream",
    "prompt_confirm",
    "prompt_string",
    "prompt_list",
    "llm_response",
    "llm_json",
    "num_tokens",
    "is_token_overflow",
]


def announce(message, prefix: str = ""):
    # Function to print a colored message
    cyan = '\033[96m'
    default = '\033[0m'
    print("{0}{1}{2}{3}".format(prefix, cyan, message, default))
    logging.info(f"{prefix}{message}")


def stream(message, prefix: str = ""):
    # Function to print a colored message
    cyan = '\033[96m'
    default = '\033[0m'
    print("{0}{1}{2}{3}".format(prefix, cyan, message, default), end="")
    sys.stdout.flush()
    logging.info(f"{prefix}{message}")


def prompt_confirm(question_message, default=True):
    # Function to prompt a confirmation question

    result = prompt(
        {
            'type': 'confirm',
            'name': 'name',
            'message': question_message,
            'default': default
        }
    ).get('name')
    logging.info(f"Confirmation prompt: {question_message}, result: {result}")
    return result


def prompt_string(question_message, default=None):
    # Function to prompt a string input question

    result = prompt(
        {
            'type': 'input',
            'name': 'name',
            'message': question_message,
            'default': default if default else ""
        }
    ).get('name')
    logging.info(f"String prompt: {question_message}, result: {result}")
    return result


def prompt_list(question_message, choices, default=None):
    # Function to prompt a list selection question
    result = prompt(
        {
            'type': 'list',
            'name': 'name',
            'message': question_message,
            'choices': choices,
            'default': default
        }
    ).get('name')
    logging.info(f"List prompt: {question_message}, result: {result}")
    return result


def llm_response(obj: any) -> str:
    """
    Extracts the top result from the LLM output
    """

    try:
        # Get the content of the first choice in the LLM output
        result = obj["choices"][0]["message"]["content"]
        logging.info(f"LLM response: {result}")
        return result
    except KeyError:
        # Return None if the required keys are not found
        logging.error("KeyError in LLM response")
        return None


def llm_json(obj: any):
    """
    Extracts the top result from the LLM output
    and converts it to JSON
    """

    try:
        # Get the content of the first choice in the LLM output
        result = obj["choices"][0]["message"]["content"]
        # Convert the content to JSON and return it
        json_result = json.loads(result)
        logging.info(f"LLM JSON response: {json_result}")
        return json_result
    except (KeyError, json.JSONDecodeError):
        # Return None if the required keys are not found or if the content is not valid JSON
        logging.error("Error in LLM JSON response")
        return None

encoding_4 = tiktoken.encoding_for_model("gpt-4")
encoding_3_5 = tiktoken.encoding_for_model("gpt-3.5-turbo")

def num_tokens(content: str, model="gpt-4"):
    if model == "gpt-3.5-turbo":
        encoding = encoding_3_5
    else:
        encoding = encoding_4

    token_count = len(encoding.encode(content))
    logging.info(f"Number of tokens for content: {token_count}")
    return token_count


def is_token_overflow(content: str, model="gpt-4"):
    if model == "gpt-3.5-turbo":
        max_tokens = 3900
    else:
        max_tokens = 8000
    token_overflow = num_tokens(content, model=model) > max_tokens
    if token_overflow:
        logging.warning(f"Token overflow detected: {content}")
    return token_overflow