import logging
from openai import ChatCompletion

from .utils import stream

__all__ = [
    "ChatBot"
]

class ChatBot():

    def __init__(self, content):
        self.content = content
        self.messages = [
            {"role": "system", "content": "You are a highly intelligent investment analyst. You prioritize quantitative analysis and accurate data. Respond based on the content from the file and the user prompt."},
            {"role": "user", "content": f"Content:\n\n{content}"}
        ]

    def send(self, prompt: str):
        try:
            self.messages.append({"role": "user", "content": f"Prompt: {prompt}"})
            response = ChatCompletion.create(
                model="gpt-4",
                messages=self.messages,
                temperature=0.1,
                stream=True
            )

            completion_text = ""
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

                completion_text += event_text
                stream(event_text)

            self.messages.append({"role": "assistant", "content": completion_text})

        except Exception as e:
            logging.error(f"Error generating response: {e}")
            return "An error occurred while generating the response. Please try again."