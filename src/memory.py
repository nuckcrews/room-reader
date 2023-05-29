from openai import ChatCompletion
from .extract import Extractor
from .utils import is_token_overflow, llm_response

__all__ = [
    "Memory"
]

class Memory():

    def __init__(self, system_prompt, content_path):
        self.system_message = { "role": "system", "content": system_prompt }
        self.content_path = content_path
        self.content = None
        self.chat_messages = []


    def initialize(self):
        self.content = Extractor(self.content_path).extract()

    def content_message(self):
        return {"role": "user", "content": f"Content:\n\n{self.content}"}

    def context(self):
        new_context = [self.system_message, self.content_message(), *self.chat_messages]

        is_overflow = is_token_overflow(
            "".join([message["content"] for message in new_context])
        )
        while is_overflow:
            self._remove_earliest_chat()
            new_context = [
                self.system_message,
                self.content_message(),
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

    def _create_memory_prompt(self):
        response = ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self._memory_context(),
            temperature=0
        )

        return llm_response(response)

    def _memory_context(self):
        messages = [message["content"] for message in self.chat_messages]

        is_overflow = is_token_overflow(
            "; ".join(messages),
            model="gpt-3.5-turbo"
        )
        while is_overflow:
            messages.pop(0)
            is_overflow = is_token_overflow(
                "; ".join(messages),
                model="gpt-3.5-turbo",
            )

        message_history = "; ".join(messages)

        return [
            {
                "role": "system",
                "content": "Write a short prompt for a semantic file search query based on the chat messages. Prioritize the latest messages. Output only the prompt.",
            },
            {
                "role": "user",
                "content": f"Messages:\n\n{message_history}"
            }
        ]
