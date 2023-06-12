import os
import anthropic
from .memory import Memory
from .utils import *

__all__ = ["ThropicBot"]


class ThropicBot:
    def __init__(self, content_path: str):
        self.memory = Memory("You are a highly intelligent investment analyst. You prioritize quantitative analysis and accurate data. Respond based on the content from the file and the user prompt.", content_path)
        self.memory.initialize()
        self.client = anthropic.Client(os.environ['ANTHROPIC_API_KEY'])

    def send(self, prompt: str):
        self.memory.add_chat(prompt)

        response = self.client.completion(
            prompt=f"{anthropic.HUMAN_PROMPT} {self.context()} {anthropic.AI_PROMPT}",
            model="claude-1",
            max_tokens_to_sample=2000,
        )

        print(response)
        self.memory.add_bot_chat(response)

    def context(self):
        full_context = []
        for message in self.memory.context():
            if message["role"] == "system":
                full_context.append(f"System message: {message}")
            elif message["role"] == "user":
                full_context.append(f"User message: {message}")
            elif message["role"] == "assistant":
                full_context.append(f"Assistant message: {message}")
        return "\n".join(full_context)
