# utils/ollama_manager.py

import requests
import subprocess
import time
from utils.logger import log
from config import OLLAMA_URL, OLLAMA_MODEL


def is_ollama_running():
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=3)
        return response.status_code == 200
    except:
        return False


def start_ollama_server():
    log("Starting Ollama server...")

    subprocess.Popen(["ollama", "serve"],
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL)

    # Wait until server responds
    for _ in range(10):
        time.sleep(2)
        if is_ollama_running():
            log("Ollama server started successfully.")
            return True

    log("Failed to start Ollama server.", level="ERROR")
    return False


def is_model_available(model_name):
    try:
        response = requests.get("http://localhost:11434/api/tags")
        models = response.json().get("models", [])
        return any(model_name in m["name"] for m in models)
    except:
        return False


def pull_model(model_name):
    log(f"Pulling Ollama model: {model_name}")
    subprocess.run(["ollama", "pull", model_name])


def ensure_ollama_ready():

    if not is_ollama_running():
        log("Ollama not running.")
        if not start_ollama_server():
            raise Exception("Ollama server could not be started.")

    if not is_model_available(OLLAMA_MODEL):
        log(f"Model {OLLAMA_MODEL} not found locally.")
        pull_model(OLLAMA_MODEL)

    log("Ollama is ready.")