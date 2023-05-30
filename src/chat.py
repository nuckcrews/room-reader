import logging
from openai import ChatCompletion
from .memory import Memory
from .utils import *

__all__ = ["ChatBot"]

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatBot:
    def __init__(self, content_path: str):
        self.memory = Memory("You are a highly intelligent investment analyst. You prioritize quantitative analysis and accurate data. Respond based on the content from the file and the user prompt.", content_path)
        self.memory.initialize()
        logger.info("ChatBot initialized with content path: %s", content_path)

    def send(self, prompt: str):
        self.memory.add_chat(prompt)
        logger.info("User prompt: %s", prompt)
        response = ChatCompletion.create(
            model="gpt-4",
            messages=self.memory.context(),
            temperature=0.1,
            stream=True
        )

        completion_text = ""
        stripped = False
        for event in response:
            delta = event.get("choices")[0].get("delta")
            event_text = None
            if delta:
                event_text = delta.get("content")

            if not event_text:
                continue

            if not stripped:
                event_text = event_text.strip()
                stripped = True

            completion_text += event_text
            stream(event_text)

        self.memory.add_bot_chat(completion_text)
        logger.info("Bot response: %s", completion_text)