import logging
from openai import ChatCompletion
from .memory import Memory
from .utils import *

__all__ = ["ChatBot"]


class ChatBot:
    def __init__(self, content_path: str):
        self.memory = Memory(
            [
                "You are a highly intelligent quantitative analyst who writes Python scripts for excel. You prioritize quantitative analysis and accurate data.",
                "Based on the content from the excel file, its path and user prompt, create a python script using openpyxl (it is already installed) that will run in the excel workbook.",
                "Output only the python script so that it can run right away. Make sure the code has no errors and runs smoothly."
            ],
            content_path,
        )

        self.memory.initialize()

    def send(self, prompt: str):
        self.memory.add_chat(prompt)
        response = ChatCompletion.create(
            model="gpt-4", messages=self.memory.context(), temperature=0.1, stream=True
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

            with open('./excel/script.py', 'w') as writer:
                writer.write(completion_text)

        self.memory.add_bot_chat(completion_text)
