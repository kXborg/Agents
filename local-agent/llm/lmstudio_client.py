import requests

from config import (
    LMSTUDIO_BASE_URL,
    CHAT_COMPLETIONS_ENDPOINT,
    MODEL_NAME,
    TEMPERATURE,
    MAX_TOKENS,
)

class LMStudioClient:
    def __init__(self):
        self.url = LMSTUDIO_BASE_URL + CHAT_COMPLETIONS_ENDPOINT

    def chat(self, messages, schemas):
        payload = {
            "model": MODEL_NAME,
            "messages": messages,
            "functions": schemas,
            "temperature": TEMPERATURE,
            "max_tokens": MAX_TOKENS,
        }

        response = requests.post(self.url, json=payload)

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]