import pandas as pd
import numpy as np
from openai import ChatCompletion, Completion
from openai.embeddings_utils import get_embedding, cosine_similarity
from .extract import Extractor, File
from .utils import is_token_overflow

__all__ = [
    "Memory"
]

session_memory_path = ".memory/session.csv"

class Memory():

    def __init__(self, system_prompts, content_path):
        self.system_messages = [{ "role": "system", "content": system_prompt } for system_prompt in system_prompts]
        self.content_path = content_path
        self.chat_messages = []


    def initialize(self):
        files = Extractor(self.content_path).extract()

    def context(self):
        content = Extractor(self.content_path).extract().content
        path_message = {"role": "user", "content": f"File Path:\n\n{self.content_path}"}
        path_message = {"role": "user", "content": f"File Path:\n\n{self.content_path}"}
        content_message = {"role": "user", "content": f"Content:\n\n{content}"}

        new_context = [*self.system_messages, path_message, content_message, *self.chat_messages]

        is_overflow = is_token_overflow(
            "".join([message["content"] for message in new_context])
        )
        while is_overflow:
            self._remove_earliest_chat()
            new_context = [
                *self.system_messages,
                path_message,
                content_message,
                *self.chat_messages,
            ]
            is_overflow = is_token_overflow(
                "".join([message["content"] for message in new_context])
            )

        return new_context

    def add_chat(self, chat_message):
        self.chat_messages.append({"role": "user", "content": chat_message})

    def add_bot_chat(self, bot_chat_message):
        self.chat_messages.append({"role": "assistant", "content": bot_chat_message})

    def _remove_earliest_chat(self):
        self.chat_messages.pop(0)
