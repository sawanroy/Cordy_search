# utils/llm.py

import requests
import time
from config import OLLAMA_MODEL, OLLAMA_URL
from utils.logger import log


def ask_llm(prompt: str):

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_predict": 300   # LIMIT OUTPUT TOKENS
        }
    }

    try:
        log("Sending request to Ollama...")
        start = time.time()

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=45  # HARD LIMIT
        )

        response.raise_for_status()

        end = time.time()
        log(f"Ollama responded in {round(end - start, 2)} seconds")

        result = response.json()
        return result.get("response", "")

    except Exception as e:
        log(f"LLM Error: {str(e)}", level="ERROR")
        return None