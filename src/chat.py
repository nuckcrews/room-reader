import logging
from openai import ChatCompletion
import tiktoken

from .utils import stream, llm_response

__all__ = ["ChatBot"]


class ChatBot:
    def __init__(self, content):
        self.content = content
        self.system_message = {
            "role": "system",
            "content": "You are a highly intelligent investment analyst. You prioritize quantitative analysis and accurate data. Respond based on the content from the file and the user prompt.",
        }
        self.content_message = {"role": "user", "content": f"Content:\n\n{content}"}
        self.chat_messages = []

    def send(self, prompt: str):
        try:
            self.chat_messages.append({"role": "user", "content": f"Prompt: {prompt}"})
            response = ChatCompletion.create(
                model="gpt-4",
                messages=self._context(),
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

            self.chat_messages.append({"role": "assistant", "content": completion_text})

        except Exception as e:
            logging.error(f"Error generating response: {e}")
            return "An error occurred while generating the response. Please try again."

    def _context(self):
        new_context = [self.system_message, self.content_message, *self.chat_messages]

        is_overflow = is_token_overflow(
            "".join([message["content"] for message in new_context])
        )
        while is_overflow:
            self._remove_earliest_chat()
            new_context = [
                self.system_message,
                self.content_message,
                *self.chat_messages,
            ]
            is_overflow = is_token_overflow(
                "".join([message["content"] for message in new_context])
            )

        return new_context

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


# MARK: - Helpers


encoding_4 = tiktoken.encoding_for_model("gpt-4")
encoding_3_5 = tiktoken.encoding_for_model("gpt-3.5-turbo")


def tokens(content: str, model="gpt-4"):
    if model == "gpt-3.5-turbo":
        encoding = encoding_3_5
    else:
        encoding = encoding_4

    return len(encoding.encode(content))


def is_token_overflow(content: str, model="gpt-4"):
    if model == "gpt-3.5-turbo":
        max_tokens = 3900
    else:
        max_tokens = 8000
    return tokens(content, model=model) > max_tokens
