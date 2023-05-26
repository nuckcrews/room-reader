import logging
from openai import ChatCompletion
from .utils import stream

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